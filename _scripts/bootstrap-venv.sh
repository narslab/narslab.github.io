#!/usr/bin/env bash
# Sourced by sync-papers.sh and make-thumbs.sh. Creates _scripts/.venv on first
# run (gitignored) and exports VENV_PY pointing at its interpreter.
VENV_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.venv"
VENV_PY="$VENV_DIR/bin/python"

if [ ! -x "$VENV_PY" ]; then
    echo "Creating $VENV_DIR ..." >&2
    python3 -m venv "$VENV_DIR"
    "$VENV_PY" -m pip install --quiet --upgrade pip
    "$VENV_PY" -m pip install --quiet requests pymupdf pillow
fi
export VENV_PY
