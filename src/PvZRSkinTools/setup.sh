#!/usr/bin/env bash
set -e

if [[ -z "${CI:-}" ]]; then
  trap '
    tput bel
    echo "Error occurred! Press Enter to exit..."
    read
  ' ERR
fi

uv sync

uv run python scripts/fetch_python_licenses.py

uv run python scripts/download_alacritty.py

uv run python scripts/download_spine_converter.py

uv run python scripts/generate_icon.py

if [[ "${INTERACTIVE:-1}" = "1" && -z "${CI:-}" ]]; then
    read -p "Setup finished. Press Enter to exit..."
fi
