#!/usr/bin/env bash
set -e

trap 'echo "Error occurred! Press Enter to exit..."; read' ERR

rm -rf build/PvZRSkinTools

uv run nuitka --standalone \
  --user-package-configuration-file=package-config.yaml \
  --enable-plugin=tk-inter \
  --include-package=UnityPy \
  --include-package-data=UnityPy \
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

mv build/PvZRSkinTools.dist build/PvZRSkinTools

tput bel

read -p "Build finished. Press Enter to exit..."
