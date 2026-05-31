#!/usr/bin/env bash
set -e

trap 'echo "Error occurred! Press Enter to exit..."; read' ERR

uv run nuitka --standalone \
  --enable-plugin=tk-inter \
  --include-package=UnityPy \
  --include-package-data=UnityPy \
  --include-data-file=.venv/Lib/site-packages/fmod_toolkit/libfmod/Windows/x64/fmod.dll=fmod_toolkit/libfmod/Windows/x64/fmod.dll \
  --include-package-data=archspec \
  --noinclude-dlls=libcrypto-3-x64.dll \
  --noinclude-dlls=libssl-3-x64.dll \
  --nofollow-import-to=PIL._avif \
  --nofollow-import-to=PIL._webp \
  --nofollow-import-to=PIL._imagingft \
  --nofollow-import-to=PIL._imagingtk \
  --remove-output \
  --output-dir=build \
  --output-folder-name=PvZRSkinTools \
  --output-filename=PvZRSkinTools.exe \
  src/main.py

tput bel

read -p "Build finished. Press Enter to exit..."
