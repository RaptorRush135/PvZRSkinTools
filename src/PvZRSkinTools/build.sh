#!/usr/bin/env bash
set -e

if [[ -z "${CI:-}" ]]; then
  trap '
    tput bel
    echo "Error occurred! Press Enter to exit..."
    read
  ' ERR
fi

VERSION=$(
  uv run python -c '
from importlib.metadata import version
print(version("pvzrskintools"))
')
PRODUCT_VERSION=$(uv run python scripts/get_product_version.py)

echo "Building..."
echo "Version: $VERSION"
echo "Product Version: $PRODUCT_VERSION"

rm -rf build/PvZRSkinTools
rm -rf build/PvZRSkinTools.build
rm -rf build/PvZRSkinTools.dist

INTERACTIVE=0 bash setup.sh

uv run nuitka --standalone \
  --user-package-configuration-file=package-config.yaml \
  --windows-icon-from-ico=build/cache/icon.ico \
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

echo "Copying include files..."
cp -r include/* build/PvZRSkinTools/
cp -r build/include/tools build/PvZRSkinTools/
cp -r build/include/CPython-License.rst build/PvZRSkinTools/
cp -r build/include/Python-License.txt build/PvZRSkinTools/

echo "Adding icon to launcher..."
npx --yes resedit-cli \
  build/PvZRSkinTools/tools/alacritty.exe build/PvZRSkinTools/tools/alacritty.exe \
  --icon 257,build/cache/icon.ico

echo "Generating third-party licenses..."
uv run pip-licenses --format=plain-vertical \
  --with-license-file --no-license-path \
  --output-file build/PvZRSkinTools/THIRD_PARTY_LICENSES.txt


echo "Build finished..."

if [[ -z "${CI:-}" ]]; then
  tput bel
  read -p "Press Enter to exit..."
fi
