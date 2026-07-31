# Papers workflow

The papers section is generated from the **Publications** collection in Jimi's
Zotero library. Two scripts do the work; both are idempotent, so re-running them
is always safe.

## One-time setup

```sh
cp _scripts/.env.zotero.example _scripts/.env.zotero
$EDITOR _scripts/.env.zotero          # paste a read-only key from
                                      # https://www.zotero.org/settings/keys
```

The library id and collection key are non-secret and live in `sync-papers.sh`.
On first run the scripts create `_scripts/.venv` and install their dependencies
(`requests`, `pymupdf`, `pillow`). Both the venv and the key file are
gitignored.

## Routine update

```sh
./_scripts/sync-papers.sh --dry-run     # preview
./_scripts/sync-papers.sh --overwrite   # write papers/_posts/
./_scripts/make-thumbs.sh               # fill in missing images/papers/
bundle exec jekyll build
```

### `sync-papers.sh` → `papers/_posts/*.md`

Pulls every item in the collection and writes a post with the frontmatter the
`paper` layout expects. Two behaviours worth knowing:

- **Posts are matched by DOI**, so retitling a paper in Zotero updates the post
  in place instead of creating a second one at a new permalink.
- **Hand-edited link fields are never cleared.** If you set `github:`,
  `website:`, `image:`, `pdf:` or `supplement:` by hand, a re-sync leaves it
  alone. Anything else is regenerated from Zotero, so fix metadata *there*.

It also caches the raw Zotero payload to `_scripts/.zotero-cache.json`, which
`make-thumbs.sh` reads to locate PDF attachments.

### `make-thumbs.sh` → `images/papers/*`

Gives every post a thumbnail, from the first of these that works:

1. The **first captioned figure** in the paper's PDF. Anchoring on a `Figure N`
   caption is what keeps journal adverts, mastheads and cover art out of the
   grid, and Figure 1 is almost always the framework diagram or study area —
   the most legible thing at thumbnail size.
2. A **generated cover card**: title and venue on a deep panel with a faint
   network motif, coloured deterministically from the post slug.

Useful flags: `--force` (redo existing), `--only 2026` (filter by stem),
`--cards-only`, `--dry-run`.

## Adding a PDF

Drop it in `pdfs/papers/` named for the post, then re-run:

```
pdfs/papers/2026-arabi-typology-us-transit.pdf              # <year>-<author>-<slug>
pdfs/papers/2026-arabi-typology-us-transit-supplement.pdf   # optional supplement
```

The full post stem (`2026-01-01-arabi-…`) works too. That one file gets you all
three of a real figure thumbnail, a PDF link on the paper page, and a supplement
link if present — no frontmatter editing. `_scripts/paper-pdfs.yml` is an escape
hatch for a PDF that must keep some other filename.

## Superseded

`bib-generator.r` and `papers/Publications.csv` are the old workflow: export a
CSV from Zotero by hand, then hit CrossRef for each DOI. `zotero_sync.py`
replaces both and no longer needs the CSV. They are kept only for reference.
