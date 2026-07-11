#!/usr/bin/env bash
set -e

if [[ -z "${CI:-}" ]]; then
  trap '
    tput bel
    echo "Error occurred! Press Enter to exit..."
    read
  ' ERR
else
  trap 'echo "::error::Script failed at line $LINENO"' ERR
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

NUITKA_CI_FLAGS=()
if [[ -n "${CI:-}" ]]; then
  NUITKA_CI_FLAGS+=(--assume-yes-for-downloads --show-progress --show-scons)
fi

uv run nuitka --standalone \
  "${NUITKA_CI_FLAGS[@]}" \
  --user-package-configuration-file=package-config.yaml \
  --user-plugin=scripts/unitypy_nuitka_plugin.py \
  --windows-icon-from-ico=build/cache/icon.ico \
  --enable-plugin=tk-inter \
  --include-package=UnityPy.resources \
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

EXE_PATH="build/PvZRSkinTools.dist/PvZRSkinTools.exe"

if [[ ! -f "$EXE_PATH" ]]; then
  echo "::error::Build failed — $EXE_PATH was not produced" >&2
  exit 1
fi

mv build/PvZRSkinTools.dist build/PvZRSkinTools

echo "Copying include files..."
cp -r ../../LICENSE build/PvZRSkinTools/PvZRSkinTools-License.txt
cp -r ../../README.md build/PvZRSkinTools/
cp -r include/* build/PvZRSkinTools/
cp -r build/include/tools build/PvZRSkinTools/
cp -r build/include/CPython-License.rst build/PvZRSkinTools/
cp -r build/include/Python-License.txt build/PvZRSkinTools/

echo "Adding icon to launcher..."
npm --prefix ./node-tools run set-launcher-icon

echo "Generating third-party licenses..."
uv run pip-licenses --format=plain-vertical \
  --with-license-file --no-license-path \
  --output-file build/PvZRSkinTools/THIRD_PARTY_LICENSES.txt


echo "Build finished..."

if [[ -z "${CI:-}" ]]; then
  tput bel
  read -p "Press Enter to exit..."
fi
