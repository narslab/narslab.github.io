#!/usr/bin/env bash
# Generate images/papers/ thumbnails for every paper post and point each post's
# `image:` frontmatter at the result. Run after sync-papers.sh.
#
# Usage:
#   ./_scripts/make-thumbs.sh                 # fill in whatever is missing
#   ./_scripts/make-thumbs.sh --force         # regenerate everything
#   ./_scripts/make-thumbs.sh --only 2026     # just the 2026 posts
set -euo pipefail
cd "$(dirname "$0")"

source ./bootstrap-venv.sh
exec "$VENV_PY" paper_thumbs.py "$@"
