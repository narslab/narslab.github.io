#!/usr/bin/env python3
"""Generate Jekyll paper posts directly from the Zotero "Publications" collection.

This replaces the manual "export Publications.csv from Zotero, then run
bib-generator.r" workflow: it pulls items straight from the Zotero Web API and
writes theme-compliant markdown into papers/_posts/.

The frontmatter matches what the `paper` layout and papers/index.html expect
(layout, title, image, authors, year, ref, journal, volume, pdf, doi, github)
followed by an `# Abstract` body.

Two things are deliberately conservative:

  * Existing posts are matched by DOI first, so a post keeps its filename (and
    therefore its permalink) even if the Zotero title is later reworded.
  * Hand-edited link fields (image, pdf, github, website, supplement) are never
    blanked out by a re-sync -- whatever is already in the file wins.

Configuration comes from environment variables (never hardcode your key):

    ZOTERO_LIBRARY_ID     required  numeric library id
    ZOTERO_LIBRARY_TYPE   optional  "user" (default) or "group"
    ZOTERO_API_KEY        required for private libraries
    ZOTERO_COLLECTION_KEY optional  restrict to one collection (recommended)

Find your library id + create a key at https://www.zotero.org/settings/keys
(the "userID for use in API calls" is your ZOTERO_LIBRARY_ID for a user library).

Usage (see also sync-papers.sh, which sets the environment for you):
    python3 zotero_sync.py                 # create missing posts; report diffs & orphans
    python3 zotero_sync.py --overwrite     # also rewrite existing posts that changed
    python3 zotero_sync.py --dry-run       # show what would happen, write nothing
"""

import argparse
import json
import os
import re
import sys

import requests

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(REPO_ROOT, "papers", "_posts")
PDF_DIR = os.path.join(REPO_ROOT, "pdfs", "papers")
IMAGE_DIR = os.path.join(REPO_ROOT, "images", "papers")
CACHE_PATH = os.path.join(REPO_ROOT, "_scripts", ".zotero-cache.json")

API_ROOT = "https://api.zotero.org"
PAGE_SIZE = 100

# Item types that are not publications (skip these entirely).
SKIP_TYPES = {"attachment", "note", "annotation"}

# Only files named like a Jekyll post are ours to manage. This leaves
# example-*.md and any other scratch file in papers/_posts/ alone.
POST_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")

# Link fields that a human may have filled in by hand. A re-sync only ever adds
# to these, never clears them.
PRESERVED_FIELDS = ("image", "pdf", "github", "website", "supplement")

STOPWORDS = {
    "in", "for", "and", "a", "an", "the", "of", "on", "this", "to",
    "who", "whom", "whose", "why", "how", "where", "is", "my", "from",
}

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def fix_datestring(d):
    """Normalise a free-form Zotero date into the yyyy-mm-dd a post filename needs.

    Zotero dates come in many shapes ("2019-09", "December 1, 2015",
    "2019/11/00"). Returns "" if nothing matches, so the caller can warn.
    """
    d = (d or "").strip()
    if not d:
        return ""

    def clamp(part):  # "00"/"0" -> "01"; otherwise zero-pad
        return "01" if part in ("0", "00") else part.zfill(2)

    # YYYY-MM-DD or YYYY/MM/DD (day/month may be 00 when only partly known)
    m = re.match(r"^([0-9]{4})[-/]([0-9]{1,2})[-/]([0-9]{1,2})", d)
    if m:
        return f"{m.group(1)}-{clamp(m.group(2))}-{clamp(m.group(3))}"
    # YYYY-MM or YYYY/MM
    m = re.match(r"^([0-9]{4})[-/]([0-9]{1,2})$", d)
    if m:
        return f"{m.group(1)}-{clamp(m.group(2))}-01"
    # YYYY
    if re.match(r"^[0-9]{4}$", d):
        return d + "-01-01"

    # MM/DD/YYYY (US order -- first group is 1-2 digits, so no clash with above)
    m = re.match(r"^([0-9]{1,2})/([0-9]{1,2})/([0-9]{2,4})", d)
    if m:
        month, day, year = clamp(m.group(1)), clamp(m.group(2)), m.group(3)
        if len(year) < 4:
            year = ("20" + year) if int(year) < 30 else ("19" + year)
        return f"{year}-{month}-{day}"

    # "December 19, 2019" / "Dec 19 2019"
    m = re.match(r"([A-Za-z.]+)\s+([0-9]{1,2}),?\s+([0-9]{4})", d)
    if m and m.group(1)[:3].lower() in MONTHS:
        return f"{m.group(3)}-{MONTHS[m.group(1)[:3].lower()]:02}-{int(m.group(2)):02}"

    # "September 2024" (month + year, no day)
    m = re.match(r"([A-Za-z.]+)\s+([0-9]{4})$", d)
    if m and m.group(1)[:3].lower() in MONTHS:
        return f"{m.group(2)}-{MONTHS[m.group(1)[:3].lower()]:02}-01"

    return d  # unrecognised -- caller warns


def fetch_items(library_type, library_id, api_key, collection_key):
    """Return every item's `data` dict from the library/collection, paginated."""
    base = f"{API_ROOT}/{library_type}s/{library_id}"
    url = f"{base}/collections/{collection_key}/items" if collection_key else f"{base}/items"
    headers = {"Zotero-API-Version": "3"}
    if api_key:
        headers["Zotero-API-Key"] = api_key

    items, start = [], 0
    while True:
        resp = requests.get(
            url,
            headers=headers,
            params={"format": "json", "include": "data", "limit": PAGE_SIZE, "start": start},
            timeout=30,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        items.extend(entry["data"] for entry in batch)
        total = int(resp.headers.get("Total-Results", "0"))
        start += PAGE_SIZE
        if start >= total:
            break
    return items


def format_authors(creators):
    """"Last, First" Zotero creators -> ("First Last, First Last", ["Last", ...])."""
    names, last_names = [], []
    for c in creators or []:
        if c.get("creatorType") != "author":
            continue
        if "name" in c:  # single-field creator (institution etc.)
            names.append(c["name"])
            last_names.append(c["name"])
            continue
        last = c.get("lastName", "").strip()
        first = c.get("firstName", "").strip()
        names.append(f"{first} {last}".strip())
        last_names.append(last)
    return ", ".join(names), last_names


def asset_lookup(stem, names, prefix, suffix=""):
    """Find an asset filed under a post's stem, tolerating a year-only prefix.

    Post stems carry a full date because Jekyll requires it, but PDFs are filed
    by year alone -- pdfs/papers/2026-arabi-typology-us-transit.pdf serves the
    post 2026-01-01-arabi-typology-us-transit. Accept either spelling.
    """
    short = re.sub(r"^(\d{4})-\d{2}-\d{2}-", r"\1-", stem)
    for candidate in dict.fromkeys([stem, short]):
        key = f"{candidate}{suffix}".lower()
        if key in names:
            return f"{prefix}/{names[key]}"
    return ""


def slug_from_title(title):
    words = [w.lower() for w in title.split(" ")]
    words = [w for w in words if w not in STOPWORDS][:3]
    words = [re.sub(r"[^\w]", "", w) for w in words]
    return "-".join(w for w in words if w)


def citation_ref(last_names, year, venue):
    """Short inline citation shown on the papers index, e.g. "Oke et al. 2020. TR-A"."""
    if len(last_names) > 2:
        who = f"{last_names[0]} et al."
    elif len(last_names) == 2:
        who = f"{last_names[0]} and {last_names[1]}"
    elif last_names:
        who = last_names[0]
    else:
        who = ""
    short_venue = venue.split(":")[0].strip()
    return " ".join(p for p in (who, f"{year}." if year else "", short_venue) if p).rstrip(". ")


def parse_frontmatter(text):
    """Return {field: raw value string} for the top-level scalars of a post."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        fm = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if fm:
            out[fm.group(1)] = fm.group(2).strip()
    return out


def build_post(data, existing_by_doi, pdf_names, image_names):
    """Return (filename, content, warning) for a Zotero item, or None to skip."""
    if data.get("itemType", "") in SKIP_TYPES:
        return None
    title = data.get("title", "").strip()
    if not title:
        return None

    authors, last_names = format_authors(data.get("creators"))
    first_last = last_names[0] if last_names else "anon"
    raw_date = data.get("date", "")
    date = fix_datestring(raw_date)
    year = date[:4] if re.match(r"^[0-9]{4}", date) else ""
    doi = data.get("DOI", "").strip()
    url = data.get("url", "").strip()
    abstract = data.get("abstractNote", "").strip()
    item_type = data.get("itemType", "")

    # Venue + volume/issue/pages, formatted the way _layouts/paper.html renders it.
    if item_type == "report":
        venue = data.get("institution") or data.get("publisher") or ""
        number = data.get("reportNumber") or data.get("number") or ""
        volume = ""
        journal = f"{venue} {number}.".strip() if number else f"{venue}.".strip()
    else:
        venue = data.get("publicationTitle") or data.get("proceedingsTitle") or ""
        volume = (data.get("volume") or "").strip()
        issue = (data.get("issue") or "").strip()
        pages = (data.get("pages") or "").strip().replace("--", "-")
        locator = volume
        if issue:
            locator += f"({issue})"
        if pages:
            locator = f"{locator}:{pages}" if locator else pages
        journal = f"{venue} {locator}.".strip() if locator else f"{venue}.".strip()

    slug = f"{first_last}-{slug_from_title(title)}".lower()
    slug = re.sub(r"[^\w-]", "", slug.replace(" ", "-"))
    name = f"{date}-{slug}" if date else slug

    # A DOI we already have on disk keeps its existing filename, so permalinks
    # survive a Zotero retitling.
    filename = existing_by_doi.get(doi.lower()) if doi else None
    filename = filename or f"{name}.md"
    stem = filename[:-3]

    fields = {
        "layout": "paper",
        "title": f'"{title}"',
        "image": asset_lookup(stem, image_names, "/images/papers"),
        "authors": authors,
        "year": year,
        "ref": citation_ref(last_names, year, venue),
        "journal": f'"{journal}"',
        "volume": volume,
        "pdf": asset_lookup(stem, pdf_names, "/pdfs/papers"),
        "supplement": asset_lookup(stem, pdf_names, "/pdfs/papers", "-supplement"),
        "doi": doi,
        "github": "",
    }
    # A DOI-less item links out via `website:`, but only if Zotero holds a real
    # absolute URL -- publisher exports sometimes leave a site-relative path.
    if not doi and url.startswith("http"):
        fields["website"] = url

    warning = None
    if not date:
        warning = f"{filename}: could not parse date {raw_date!r}"
    elif not venue:
        warning = (f"{filename}: no publisher/institution in Zotero -- "
                   f"citation line will be bare")
    elif not doi and url and not url.startswith("http"):
        warning = f"{filename}: Zotero URL is not absolute ({url!r}) -- dropped; fix in Zotero"

    return filename, fields, abstract, warning


def render_post(fields, abstract):
    lines = ["---"]
    lines += [f"{k}: {v}".rstrip() for k, v in fields.items()]
    lines += ["---", "", "# Abstract", "", abstract, ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--overwrite", action="store_true",
                    help="rewrite existing posts whose generated content changed")
    ap.add_argument("--dry-run", action="store_true",
                    help="report actions without writing anything")
    ap.add_argument("--output-dir", default=POSTS_DIR,
                    help="where to write posts (default: papers/_posts)")
    ap.add_argument("--verbose", action="store_true",
                    help="print each post's raw Zotero date -> normalized date")
    args = ap.parse_args()

    library_id = os.environ.get("ZOTERO_LIBRARY_ID")
    if not library_id:
        sys.exit("ZOTERO_LIBRARY_ID is not set. Run ./_scripts/sync-papers.sh instead, "
                 "or see the header of this file.")
    library_type = os.environ.get("ZOTERO_LIBRARY_TYPE", "user")
    api_key = os.environ.get("ZOTERO_API_KEY")
    collection_key = os.environ.get("ZOTERO_COLLECTION_KEY")

    posts_dir = args.output_dir
    os.makedirs(posts_dir, exist_ok=True)

    # Index what is already on disk: DOI -> filename, plus the preserved link
    # fields so a re-sync never blanks a hand-edited value.
    existing_by_doi, existing_text, preserved = {}, {}, {}
    for f in os.listdir(posts_dir):
        if not POST_RE.match(f):
            continue
        with open(os.path.join(posts_dir, f), encoding="utf-8") as fh:
            text = fh.read()
        existing_text[f] = text
        fm = parse_frontmatter(text)
        doi = fm.get("doi", "").strip().lower()
        if doi:
            existing_by_doi[doi] = f
        preserved[f] = {k: fm[k] for k in PRESERVED_FIELDS if fm.get(k, "").strip()}

    def by_stem(directory, exts):
        found = {}
        if os.path.isdir(directory):
            for f in os.listdir(directory):
                stem, ext = os.path.splitext(f)
                if ext.lower() in exts:
                    found[stem.lower()] = f
        return found

    pdf_names = by_stem(PDF_DIR, {".pdf"})
    image_names = by_stem(IMAGE_DIR, {".png", ".jpg", ".jpeg"})

    try:
        items = fetch_items(library_type, library_id, api_key, collection_key)
    except requests.HTTPError as e:
        sys.exit(f"Zotero API error: {e} (check library id/type/key/collection)")

    # Cache the raw payload so paper_thumbs.py can resolve PDF attachments
    # without a second round trip (and works offline afterwards).
    if not args.dry_run:
        with open(CACHE_PATH, "w", encoding="utf-8") as fh:
            json.dump(items, fh, indent=1)

    created, updated, unchanged, warnings, dates = [], [], [], [], []
    generated = set()

    for data in items:
        result = build_post(data, existing_by_doi, pdf_names, image_names)
        if result is None:
            continue
        filename, fields, abstract, warning = result
        if warning:
            warnings.append(warning)
        dates.append(f"{filename[:-3]:58s} {data.get('date', '')!r:22} -> {fields['year'] or '(unparsed)'}")

        # Never clear a link field a human filled in.
        for k, v in preserved.get(filename, {}).items():
            fields[k] = v

        content = render_post(fields, abstract)
        generated.add(filename)
        path = os.path.join(posts_dir, filename)
        old = existing_text.get(filename)

        if old is None:
            created.append(filename)
            if not args.dry_run:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(content)
        elif old.rstrip() != content.rstrip():
            if args.overwrite:
                updated.append(filename)
                if not args.dry_run:
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(content)
            else:
                updated.append(filename + "  (differs -- rerun with --overwrite)")
        else:
            unchanged.append(filename)

    orphans = sorted(set(existing_text) - generated)

    def report(label, rows):
        print(f"\n{label} ({len(rows)}):")
        for r in sorted(rows):
            print(f"  {r}")

    print("=" * 68)
    print(f"Zotero sync -- {len(items)} items fetched"
          + (" [DRY RUN]" if args.dry_run else ""))
    print("=" * 68)
    if args.verbose:
        report("Dates (raw -> year)", dates)
    report("Created", created)
    report("Updated", updated)
    print(f"\nUnchanged: {len(unchanged)}")
    if orphans:
        report("Orphaned posts (no matching Zotero item -- delete by hand if stale)", orphans)
    if warnings:
        report("WARNING", warnings)
    print("\nNext: ./_scripts/make-thumbs.sh   (generates images/papers/ thumbnails)\n")


if __name__ == "__main__":
    main()
