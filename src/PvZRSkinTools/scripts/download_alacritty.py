from pathlib import Path
from urllib.request import urlretrieve

REPO_URL = (
    "https://github.com/alacritty/alacritty"
    "/releases/download/v0.17.0/Alacritty-v0.17.0-portable.exe"
)
EXE_NAME = "alacritty.exe"

LICENSE_URL = (
    "https://raw.githubusercontent.com/alacritty/alacritty"
    "/refs/heads/master/LICENSE-APACHE"
)
LICENSE_NAME = "Alacritty-License.txt"

OUTPUT_DIR = Path("build/include/tools")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

exe_dest = OUTPUT_DIR / EXE_NAME
license_dest = OUTPUT_DIR / LICENSE_NAME

if exe_dest.exists():
    print(f"  Skipping download, already exists: {exe_dest}")
else:
    print(f"  Downloading {REPO_URL}...")
    urlretrieve(REPO_URL, exe_dest)
    print(f"  Saved to {exe_dest}")

if license_dest.exists():
    print(f"  Skipping download, already exists: {license_dest}")
else:
    print(f"Downloading {LICENSE_URL}...")
    urlretrieve(LICENSE_URL, license_dest)
    print(f"  Saved to {license_dest}")
