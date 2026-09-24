from pathlib import Path
from urllib.request import urlretrieve

RELEASE_VERSION = "3.8"
REPO_URL = (
    "https://github.com/wang606/SpineSkeletonDataConverter"
    f"/releases/download/v{RELEASE_VERSION}/SpineSkeletonDataConverter.exe"
)

exe_path = Path(f"build/cache/SpineSkeletonDataConverter-v{RELEASE_VERSION}.exe")
target_path = Path("build/include/tools/SpineSkeletonDataConverter.exe")

exe_path.parent.mkdir(parents=True, exist_ok=True)
target_path.parent.mkdir(parents=True, exist_ok=True)

if not exe_path.exists():
    print(f"  Downloading {REPO_URL}...")
    urlretrieve(REPO_URL, exe_path)
else:
    print(f"  Skipping download, already exists: {exe_path}")

target_path.write_bytes(exe_path.read_bytes())
