import os
import subprocess
import sys

from src.paths import IS_BUILD, TOOLS_DIR


RELAUNCH_ENV_VAR = "PVZRSKINTOOLS_RELAUNCH"


def ensure_relaunch() -> None:
    if (
        sys.platform != "win32"
        or not IS_BUILD
        or os.environ.get(RELAUNCH_ENV_VAR) == "1"
    ):
        return

    env = os.environ.copy()
    env[RELAUNCH_ENV_VAR] = "1"

    # pylint: disable=consider-using-with
    subprocess.Popen(
        [
            TOOLS_DIR / "alacritty.exe",
            "--config-file",
            str(TOOLS_DIR / "alacritty.toml"),
            "--command",
            sys.argv[0],
        ],
        env=env,
    )

    os._exit(0)


def set_title(title: str) -> None:
    if sys.platform == "win32":
        os.system(f"title {title}")
