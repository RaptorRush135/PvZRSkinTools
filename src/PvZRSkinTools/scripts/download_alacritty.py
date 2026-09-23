from pathlib import Path
from urllib.request import urlretrieve

DOWNLOADS = [
    (
        (
            "https://github.com/alacritty/alacritty"
            "/releases/download/v0.17.0/Alacritty-v0.17.0-portable.exe"
        ),
        "alacritty.exe",
    ),
    (
        (
            "https://raw.githubusercontent.com/alacritty/alacritty"
            "/refs/heads/master/LICENSE-APACHE"
        ),
        "Alacritty-License.txt",
    ),
    (
        (
            "https://raw.githubusercontent.com/alacritty/alacritty-theme"
            "/refs/heads/master/themes/afterglow.toml"
        ),
        "afterglow.toml",
    ),
    (
        (
            "https://raw.githubusercontent.com/alacritty/alacritty-theme"
            "/refs/heads/master/LICENSE"
        ),
        "Alacritty-Theme-License.txt",
    ),
]

OUTPUT_DIR = Path("build/include/tools")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def download_if_missing(download_url: str, destination: Path) -> None:
    if destination.exists():
        print(f"  Skipping download, already exists: {destination}")
        return

    print(f"  Downloading {url}...")
    urlretrieve(download_url, destination)
    print(f"  Saved to {destination}")


for url, filename in DOWNLOADS:
    download_if_missing(url, OUTPUT_DIR / filename)
