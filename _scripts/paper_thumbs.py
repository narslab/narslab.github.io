#!/usr/bin/env python3
"""Generate a thumbnail for every paper post and wire it into the frontmatter.

Two sources, in order:

  1. A PDF, if one can be found for the post. The largest coherent figure region
     in the first ~10 pages is detected (image blocks + vector drawings, merged
     into clusters) and rendered as the thumbnail. This is what makes the papers
     index look like research rather than a list.

  2. A generated cover card, when no PDF is available -- the paper's title and
     venue set on a deep panel with a faint network motif, coloured
     deterministically from the post slug so the page has variety without being
     noisy.

PDFs are looked for in this order:

  * pdfs/papers/<post-stem>.pdf                (drop one in and re-run)
  * an override in _scripts/paper-pdfs.yml     (for oddly-named existing files)
  * the PDF attachment in your local Zotero storage, resolved through the DOI
    using the cache that zotero_sync.py writes to _scripts/.zotero-cache.json

Output goes to images/papers/<post-stem>.png (or .jpg when the PNG is large),
and each post's `image:` frontmatter field is updated to point at it.

Usage (see also make-thumbs.sh, which handles the virtualenv):
    python3 paper_thumbs.py                 # fill in whatever is missing
    python3 paper_thumbs.py --force         # regenerate everything
    python3 paper_thumbs.py --cards-only    # ignore PDFs, generate cards
    python3 paper_thumbs.py --only 2026-01  # substring filter on the post stem
    python3 paper_thumbs.py --dry-run       # report only, write nothing
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(REPO_ROOT, "papers", "_posts")
PDF_DIR = os.path.join(REPO_ROOT, "pdfs", "papers")
IMAGE_DIR = os.path.join(REPO_ROOT, "images", "papers")
CACHE_PATH = os.path.join(REPO_ROOT, "_scripts", ".zotero-cache.json")
OVERRIDES_PATH = os.path.join(REPO_ROOT, "_scripts", "paper-pdfs.yml")
ZOTERO_STORAGE = os.path.expanduser("~/Zotero/storage")

POST_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")

# Thumbnails are committed to the repo, so keep them small: cap the long edge,
# and fall back to JPEG when a PNG of a photographic figure gets heavy.
MAX_EDGE = 900
PNG_SIZE_LIMIT = 300 * 1024

CARD_SIZE = (900, 675)
ACCENT = (221, 45, 45)  # $primary from css/custom.scss

# Deep, desaturated panels -- white text stays legible on all of them.
CARD_COLORS = [
    ((0x25, 0x36, 0x4A), (0x14, 0x1F, 0x2C)),  # slate
    ((0x14, 0x4B, 0x50), (0x0B, 0x2B, 0x2E)),  # teal
    ((0x3E, 0x24, 0x40), (0x24, 0x14, 0x26)),  # aubergine
    ((0x1D, 0x40, 0x35), (0x10, 0x25, 0x1E)),  # forest
    ((0x2A, 0x2E, 0x56), (0x17, 0x19, 0x30)),  # indigo
    ((0x5A, 0x22, 0x22), (0x33, 0x12, 0x12)),  # brick
    ((0x3A, 0x33, 0x1C), (0x21, 0x1D, 0x10)),  # olive
]

FONT_CANDIDATES = {
    "bold": [
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/TTF/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/gnu-free/FreeSansBold.ttf",
        "/usr/share/fonts/noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "regular": [
        "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/TTF/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/gnu-free/FreeSans.ttf",
        "/usr/share/fonts/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
}


def load_font(kind, size):
    for path in FONT_CANDIDATES[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# --------------------------------------------------------------------------
# Post parsing
# --------------------------------------------------------------------------

def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        fm = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if fm:
            out[fm.group(1)] = fm.group(2).strip().strip('"')
    return out


def set_frontmatter_field(text, field, value):
    """Set `field: value` in the frontmatter, adding it after `title:` if absent."""
    head_m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not head_m:
        return text
    head, rest = head_m.group(1), text[head_m.end():]
    lines = head.splitlines()
    for i, line in enumerate(lines):
        if re.match(rf"^{field}:", line):
            lines[i] = f"{field}: {value}"
            break
    else:
        insert_at = next((i + 1 for i, l in enumerate(lines) if l.startswith("title:")), 1)
        lines.insert(insert_at, f"{field}: {value}")
    return "---\n" + "\n".join(lines) + "\n---\n" + rest


def load_overrides():
    """Parse the flat `stem: path` map in _scripts/paper-pdfs.yml (no PyYAML needed)."""
    out = {}
    if not os.path.exists(OVERRIDES_PATH):
        return out
    with open(OVERRIDES_PATH, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if not line or ":" not in line:
                continue
            key, val = line.split(":", 1)
            val = val.strip().strip('"').strip("'")
            if val:
                out[key.strip()] = val
    return out


def normalize_title(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def zotero_pdf_index():
    """Locate PDF attachments in local Zotero storage.

    Returns (by_doi, by_title_fragment). The second index exists because an
    attachment is not always filed under the item we sync: a PDF may hang off a
    preprint or duplicate entry, and reports often carry no DOI at all. Zotero
    names its files "Authors - Year - Title.pdf", so the title fragment gives a
    reliable second chance at a match.
    """
    if not os.path.exists(CACHE_PATH):
        return {}, {}
    with open(CACHE_PATH, encoding="utf-8") as fh:
        items = json.load(fh)

    doi_by_key = {d["key"]: d["DOI"].strip().lower()
                  for d in items if d.get("DOI") and d.get("itemType") != "attachment"}

    by_doi, by_title = {}, {}
    for d in items:
        if d.get("itemType") != "attachment" or d.get("contentType") != "application/pdf":
            continue
        filename = d.get("filename", "")
        path = os.path.join(ZOTERO_STORAGE, d["key"], filename)
        if not os.path.exists(path):
            continue
        doi = doi_by_key.get(d.get("parentItem"))
        if doi:
            by_doi.setdefault(doi, path)
        # "Authors - Year - Some truncated title.pdf" -> "sometruncatedtitle"
        fragment = normalize_title(os.path.splitext(filename)[0].split(" - ")[-1])
        if len(fragment) >= 20:
            by_title.setdefault(fragment, path)
    return by_doi, by_title


def asset_names(stem):
    """Filenames (without extension) a post's assets may use.

    Post stems carry a full date because Jekyll requires it, but PDFs are filed
    by year alone -- 2026-arabi-typology-us-transit.pdf for the post
    2026-01-01-arabi-typology-us-transit. Accept both.
    """
    names = [stem]
    short = re.sub(r"^(\d{4})-\d{2}-\d{2}-", r"\1-", stem)
    if short != stem:
        names.append(short)
    return names


def find_pdf(stem, doi, title, overrides, zotero_index):
    for name in asset_names(stem):
        local = os.path.join(PDF_DIR, f"{name}.pdf")
        if os.path.exists(local):
            return local
    if stem in overrides:
        path = overrides[stem]
        path = path if os.path.isabs(path) else os.path.join(REPO_ROOT, path)
        if os.path.exists(path):
            return path

    by_doi, by_title = zotero_index
    if doi and doi.lower() in by_doi:
        return by_doi[doi.lower()]

    norm = normalize_title(title)
    for fragment, path in by_title.items():
        if norm.startswith(fragment):
            return path
    return None


# --------------------------------------------------------------------------
# Figure extraction
# --------------------------------------------------------------------------

def merge_rects(rects, gap=8):
    """Merge rectangles that touch or nearly touch, so a tiled figure comes back
    as one region rather than eighty fragments."""
    out = [fitz.Rect(r) for r in rects]
    changed = True
    while changed:
        changed = False
        for i in range(len(out)):
            for j in range(i + 1, len(out)):
                grown = fitz.Rect(out[i]) + (-gap, -gap, gap, gap)
                if grown.intersects(out[j]):
                    out[i] = out[i] | out[j]
                    del out[j]
                    changed = True
                    break
            if changed:
                break
    return out


CAPTION_RE = re.compile(r"^\s*(?:fig(?:ure)?\.?|abb\.?)\s*(\d{1,2})\b", re.I)

# Minimum share of a page an *uncaptioned* region must cover to be used.
FALLBACK_MIN_COVERAGE = 0.12


def page_regions(page):
    """Merged image + vector-drawing regions on a page that could be a figure."""
    pr = page.rect
    page_area = pr.width * pr.height
    if page_area <= 0:
        return [], page_area

    candidates = [b["bbox"] for b in page.get_text("dict")["blocks"] if b["type"] == 1]
    for dr in page.get_drawings():
        r = fitz.Rect(dr["rect"])
        if r.width < 2 or r.height < 2:
            continue
        if r.width * r.height > 0.9 * page_area:
            continue  # page-sized background fill, not a figure
        candidates.append(r)

    regions = []
    for c in merge_rects(candidates) if candidates else []:
        w, h = c.width, c.height
        if w < 0.25 * pr.width or h < 0.10 * pr.height:
            continue
        if w > 0.85 * pr.width and h > 0.85 * pr.height:
            continue  # whole-page artwork (scanned page, cover, full-page ad)
        if not 0.35 <= w / h <= 4.5:
            continue
        regions.append(c)
    return regions, page_area


def captioned_figures(page, regions):
    """Pair regions with the "Figure N" caption directly beneath them.

    Anchoring on a caption is what separates an actual figure from a journal
    advert, a masthead, or a decorative cover image -- none of which are
    captioned. Yields (figure_number, region).
    """
    out = []
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if b["type"] != 0:
            continue
        text = "".join(s["text"] for l in b["lines"] for s in l["spans"])[:40]
        m = CAPTION_RE.match(text)
        if not m:
            continue
        cap = fitz.Rect(b["bbox"])
        for r in regions:
            gap = cap.y0 - r.y1
            if not -6 <= gap <= 60:
                continue
            overlap = min(cap.x1, r.x1) - max(cap.x0, r.x0)
            if overlap < 0.35 * min(cap.width, r.width):
                continue
            out.append((int(m.group(1)), r))
    return out


def best_figure(path, max_pages=12):
    """Render a representative figure as a PIL Image, or None.

    Prefers the lowest-numbered captioned figure -- Figure 1 is nearly always
    the framework diagram, study area, or overview, which reads far better as a
    thumbnail than whichever figure happens to be largest. Falls back to the
    biggest plausible region when a PDF has no detectable captions.
    """
    doc = fitz.open(path)
    captioned, fallback = [], None

    for pno in range(min(max_pages, doc.page_count)):
        page = doc[pno]
        regions, page_area = page_regions(page)
        if not regions:
            continue

        for num, rect in captioned_figures(page, regions):
            captioned.append((num, -(rect.width * rect.height), pno, rect))

        for r in regions:
            coverage = r.width * r.height / page_area
            # Uncaptioned regions are only trustworthy when they're big. A
            # repository cover sheet (HAL, SSRN, agency reports) puts a logo on
            # page 1 that is otherwise the largest thing in the file; a real
            # figure fills much more of its page.
            if coverage < FALLBACK_MIN_COVERAGE:
                continue
            score = coverage * (1.0 - 0.02 * pno)
            if fallback is None or score > fallback[0]:
                fallback = (score, pno, r)

    if captioned:
        _, _, pno, rect = min(captioned, key=lambda t: t[:3])
    elif fallback:
        _, pno, rect = fallback
    else:
        doc.close()
        return None

    page = doc[pno]
    rect = (fitz.Rect(rect) + (-4, -4, 4, 4)) & page.rect
    pix = page.get_pixmap(clip=rect, dpi=180, colorspace=fitz.csRGB)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    doc.close()
    return img


# --------------------------------------------------------------------------
# Generated cover cards
# --------------------------------------------------------------------------

def wrap_text(draw, text, font, max_width):
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def network_motif(size, seed, color):
    """A faint node-link overlay -- a nod to the lab's network science work."""
    rng = random.Random(seed)
    w, h = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    nodes = [(rng.uniform(0, w), rng.uniform(0, h)) for _ in range(26)]
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            dist = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
            if dist < w * 0.22:
                d.line([a, b], fill=color + (26,), width=2)
    for n in nodes:
        r = rng.uniform(3, 7)
        d.ellipse([n[0] - r, n[1] - r, n[0] + r, n[1] + r], fill=color + (46,))
    return layer


def make_card(title, venue, year, seed):
    w, h = CARD_SIZE
    digest = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    top, bottom = CARD_COLORS[digest % len(CARD_COLORS)]

    card = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(card)
    for y in range(h):
        t = y / (h - 1)
        d.line([(0, y), (w, y)],
               fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))

    card = Image.alpha_composite(
        card.convert("RGBA"), network_motif((w, h), digest, (255, 255, 255))).convert("RGB")
    d = ImageDraw.Draw(card)

    pad = 64
    d.rectangle([0, 0, 14, h], fill=ACCENT)  # accent spine, echoes $primary

    # Shrink the title until it fits the available block in at most 6 lines.
    max_width = w - pad - 56
    for size in range(58, 27, -3):
        font = load_font("bold", size)
        lines = wrap_text(d, title, font, max_width)
        if len(lines) <= 6:
            break
    lines = lines[:6]
    leading = int(size * 1.22)

    meta_font = load_font("regular", 30)
    # Older posts carry literal "NA" placeholders from the retired R generator.
    venue = "" if re.fullmatch(r"(NA[\s().:]*)+", venue.strip()) else venue.split(":")[0].strip()
    meta = " · ".join(p for p in [venue, str(year)] if p)
    meta_h = int(meta_font.size * 1.4) if meta else 0

    block_h = len(lines) * leading + meta_h + (28 if meta else 0)
    y = max(pad, (h - block_h) // 2)
    for line in lines:
        d.text((pad, y), line, font=font, fill=(255, 255, 255))
        y += leading

    if meta:
        y += 28
        d.line([(pad, y - 14), (pad + 90, y - 14)], fill=ACCENT, width=4)
        d.text((pad, y), meta, font=meta_font, fill=(214, 214, 218))

    return card


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def save_thumb(img, stem, dry_run):
    """Downscale, write images/papers/<stem>.(png|jpg), return the filename."""
    img.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
    os.makedirs(IMAGE_DIR, exist_ok=True)
    png_path = os.path.join(IMAGE_DIR, f"{stem}.png")
    jpg_path = os.path.join(IMAGE_DIR, f"{stem}.jpg")

    if dry_run:
        return f"{stem}.png"

    img.save(png_path, "PNG", optimize=True)
    if os.path.getsize(png_path) > PNG_SIZE_LIMIT:
        img.convert("RGB").save(jpg_path, "JPEG", quality=85, optimize=True)
        os.remove(png_path)
        return f"{stem}.jpg"
    if os.path.exists(jpg_path):
        os.remove(jpg_path)
    return f"{stem}.png"


def existing_thumb(stem):
    for ext in (".png", ".jpg"):
        if os.path.exists(os.path.join(IMAGE_DIR, stem + ext)):
            return stem + ext
    return None


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="regenerate thumbnails that already exist")
    ap.add_argument("--cards-only", action="store_true", help="skip PDFs; generate cover cards")
    ap.add_argument("--only", default="", help="only posts whose filename contains this substring")
    ap.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    if fitz is None and not args.cards_only:
        sys.exit("PyMuPDF is not installed. Run ./_scripts/make-thumbs.sh, "
                 "or pass --cards-only to skip figure extraction.")

    overrides = load_overrides()
    zotero_index = ({}, {}) if args.cards_only else zotero_pdf_index()

    posts = sorted(f for f in os.listdir(POSTS_DIR)
                   if POST_RE.match(f) and args.only in f)

    from_figure, no_pdf, no_figure, skipped, failures = [], [], [], [], []

    for filename in posts:
        stem = filename[:-3]
        path = os.path.join(POSTS_DIR, filename)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        fm = parse_frontmatter(text)

        have = existing_thumb(stem)
        if have and not args.force:
            skipped.append(stem)
            if fm.get("image", "") != f"/images/papers/{have}" and not args.dry_run:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(set_frontmatter_field(text, "image", f"/images/papers/{have}"))
            continue

        img, pdf = None, None
        if not args.cards_only:
            pdf = find_pdf(stem, fm.get("doi", ""), fm.get("title", ""),
                           overrides, zotero_index)
            if pdf:
                try:
                    img = best_figure(pdf)
                except Exception as e:  # a malformed PDF must not stop the run
                    failures.append(f"{stem}: {type(e).__name__}: {e}")

        if img is not None:
            from_figure.append(stem)
        else:
            # Distinguish "supply a PDF and this improves" from "the PDF is
            # there but has no extractable figure" -- only the first is
            # actionable.
            (no_figure if pdf else no_pdf).append(stem)
            img = make_card(fm.get("title", stem), fm.get("journal", ""),
                            fm.get("year", ""), stem)

        out = save_thumb(img, stem, args.dry_run)

        if not args.dry_run:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(set_frontmatter_field(text, "image", f"/images/papers/{out}"))

    def report(label, rows):
        print(f"\n{label} ({len(rows)}):")
        for r in sorted(rows):
            print(f"  {r}")

    print("=" * 68)
    print(f"Paper thumbnails -- {len(posts)} posts" + (" [DRY RUN]" if args.dry_run else ""))
    print("=" * 68)
    report("From PDF figure", from_figure)
    report("Cover card -- no PDF found (supply one for a real figure)", no_pdf)
    report("Cover card -- PDF has no extractable figure", no_figure)
    print(f"\nAlready had a thumbnail: {len(skipped)}  (use --force to redo)")
    if failures:
        report("WARNING: PDF read errors", failures)
    if no_pdf:
        print("\nTo upgrade a card to a real figure, drop the paper at "
              "pdfs/papers/<year>-<author>-<slug>.pdf and re-run with --force.\n")


if __name__ == "__main__":
    main()
