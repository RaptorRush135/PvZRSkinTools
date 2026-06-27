from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile


REPO_URL = (
    "https://github.com/wang606/SpineSkeletonDataConverter"
    "/releases/download/v3.7/SpineSkeletonDataConverter.zip"
)

zip_path = Path("build/cache/SpineSkeletonDataConverter.zip")
extract_dir = Path("build/include/tools")

zip_path.parent.mkdir(parents=True, exist_ok=True)

if not zip_path.exists():
    print(f"Downloading {REPO_URL}...")
    urlretrieve(REPO_URL, zip_path)

with ZipFile(zip_path) as zip_file:
    zip_file.extract("SpineSkeletonDataConverter.exe", extract_dir)
