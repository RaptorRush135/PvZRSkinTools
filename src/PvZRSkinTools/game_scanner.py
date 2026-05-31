import os

from pathlib import Path

from file_dialog import FileDialog


SPINE_BUNDLE_PATH = Path("Replanted_Data/StreamingAssets/aa/StandaloneWindows64/spineassets_assets_assets/art/characters/spine.bundle")

def try_get_game_path() -> str | None:
    programs_path = os.getenv("ProgramFiles(x86)")
    if programs_path is None:
        return None

    path = Path(programs_path) / "Steam" / "steamapps" / "common" / "PVZ Replanted"

    if path.is_dir():
        return str(path)

    return None

def pick_spine_bundle(dialog: FileDialog) -> Path:
    initial_dir=try_get_game_path()
    while True:
        picked_dir = dialog.pick_directory("Select game directory", initial_directory=initial_dir)
        spine_bundle = picked_dir / SPINE_BUNDLE_PATH
        if not spine_bundle.is_file():
            dialog.print_warning(f"Path not found: [dim]{spine_bundle}[/dim]")
            dialog.print_warning("Select the 'PVZ Replanted' directory")
            continue

        return spine_bundle
