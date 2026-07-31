#!/usr/bin/env bash
# Pull publications from Zotero and regenerate papers/_posts/.
#
# One-time setup: create a gitignored .env.zotero next to this script with:
#     export ZOTERO_API_KEY=your-key-here
# (get a read-only key at https://www.zotero.org/settings/keys)
#
# Usage:
#   ./_scripts/sync-papers.sh --dry-run     # preview; writes nothing
#   ./_scripts/sync-papers.sh --overwrite   # apply updates to existing posts
#   ./_scripts/sync-papers.sh --overwrite && ./_scripts/make-thumbs.sh
set -euo pipefail
cd "$(dirname "$0")"

# Non-secret library config (safe to commit).
export ZOTERO_LIBRARY_ID=6356012
export ZOTERO_LIBRARY_TYPE=user
export ZOTERO_COLLECTION_KEY=GJZPZ3V3   # the "Publications" collection

if [ -f .env.zotero ]; then
    # shellcheck disable=SC1091
    source .env.zotero
fi
if [ -z "${ZOTERO_API_KEY:-}" ]; then
    echo "ZOTERO_API_KEY not set. Copy .env.zotero.example to .env.zotero and fill it in." >&2
    exit 1
fi

source ./bootstrap-venv.sh
exec "$VENV_PY" zotero_sync.py "$@"
