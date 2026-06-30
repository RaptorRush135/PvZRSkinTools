from pathlib import Path

from PIL import Image

icon = Image.open("icon/icon.png")

ICON_PATH = "build/cache/icon.ico"

Path(ICON_PATH).parent.mkdir(parents=True, exist_ok=True)

icon.save(
    ICON_PATH,
    sizes=[
        (16, 16),
        (24, 24),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256),
    ],
)

print(f"  Success: Icon saved to {ICON_PATH}")
