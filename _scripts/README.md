# Projects workflow

Every card on `/projects/` and every page under `/projects/<name>/` is generated
from a GitHub repo listed in `_config.yml`, by three scripts run in order:

```sh
GITHUB_TOKEN=$(gh auth token) bundle exec ruby _scripts/update-and-preprocess.rb
bundle exec jekyll build
```

That wrapper runs `generate-readmes.rb` (downloads each repo's `README.md` into
`projects/<name>/`), `preprocess-markdown.rb` (renames it to `index.md` and adds
the front matter the `project` layout needs), and `generate-project-data.rb`
(writes `_data/projects.yml`: description, contributors, last five commits).
The token is only needed by the last one, which uses the GitHub API.

**Commit what it generates.** `_data/projects.yml` and `projects/*/index.md` are
build inputs, not build output. The site is built by GitHub Actions from a plain
checkout, which never runs these scripts, so anything left uncommitted simply
does not exist at build time -- a project with no committed `index.md` renders
no page, and with no `_data/projects.yml` the projects page renders no cards at
all. `.gitignore` keeps everything *else* under `projects/` out.

## Adding a project

Add the repo to `readmes:` in `_config.yml`, then re-run the commands above. The
repo must be public and have a `README.md` on `main`; one that doesn't is
skipped with a message and gets no card, rather than a card linking to a 404.

`projects:` is the other list -- repos cloned in full so that pages besides the
README can be published. It is empty on purpose. A working copy runs to hundreds
of MB, must not be committed, and cannot be recreated by the CI build, so use
`readmes:` unless a project genuinely needs to publish more than its README.

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
