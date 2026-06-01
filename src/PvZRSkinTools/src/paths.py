from pathlib import Path

BASE_DIR = Path(__file__).parent

TOOLS_DIR = (BASE_DIR if "__compiled__" in globals() else BASE_DIR.parent) / "tools"
