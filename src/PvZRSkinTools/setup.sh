#!/usr/bin/env bash
set -e

trap 'echo "Error occurred! Press Enter to exit..."; read' ERR

uv sync

uv run python scripts/download_spine_converter.py

uv run python scripts/fetch_python_licenses.py

if [ "${INTERACTIVE:-1}" = "1" ]; then
    read -p "Setup finished. Press Enter to exit..."
fi
