#!/usr/bin/env bash

echo "Running Ruff..."
uv run ruff format --check .
uv run ruff check .

echo

echo "Running Pylint..."
uv run pylint src
uv run pylint scripts

read -p "Press Enter to exit..."
