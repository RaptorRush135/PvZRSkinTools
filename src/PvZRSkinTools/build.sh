#!/usr/bin/env bash
set -e

trap '
  tput bel
  echo "Error occurred! Press Enter to exit..."
  read
' ERR

VERSION=$(
  uv run python -c '
from importlib.metadata import version
print(version("pvzrskintools"))
')
PRODUCT_VERSION=$(uv run python scripts/get_nuitka_version.py)

echo "Building..."
echo "Version: $VERSION"
echo "Product Version: $PRODUCT_VERSION"

rm -rf build/PvZRSkinTools
rm -rf build/PvZRSkinTools.build
rm -rf build/PvZRSkinTools.dist

INTERACTIVE=0 bash setup.sh

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
  --product-name=PvZRSkinTools \
  --product-version="$PRODUCT_VERSION" \
  src/main.py

mv build/PvZRSkinTools.dist build/PvZRSkinTools

cp -r include/* build/PvZRSkinTools/
cp -r build/include/* build/PvZRSkinTools/

# TODO: Modify icon

uv run pip-licenses --format=plain-vertical \
  --with-license-file --no-license-path \
  --output-file build/PvZRSkinTools/THIRD_PARTY_LICENSES.txt

tput bel

read -p "Build finished. Press Enter to exit..."
