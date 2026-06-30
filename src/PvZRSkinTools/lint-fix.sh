#!/usr/bin/env bash

echo "Formatting with Ruff..."
uv run ruff format .

echo

echo "Fixing lint issues with Ruff..."
uv run ruff check --fix .

echo

echo "Running Pylint..."
uv run pylint src
uv run pylint scripts

if [[ -z "${CI:-}" ]]; then
  read -p "Press Enter to exit..."
fi
