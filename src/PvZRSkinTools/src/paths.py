from pathlib import Path

IS_BUILD = "__compiled__" in globals()

__base_dir = Path(__file__).parent.parent

BASE_DIR = __base_dir if IS_BUILD else __base_dir / "build" / "include"

TOOLS_DIR = BASE_DIR / "tools"
