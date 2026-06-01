#!/usr/bin/env bash
set -e

trap 'echo "Error occurred! Press Enter to exit..."; read' ERR

uv run python scripts/download_spine_converter.py

read -p "Setup finished. Press Enter to exit..."
