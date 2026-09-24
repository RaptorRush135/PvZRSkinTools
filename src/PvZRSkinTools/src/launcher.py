import ctypes
import os
import subprocess
import sys
from importlib.metadata import version

from src.paths import IS_BUILD, TOOLS_DIR

if sys.platform == "win32":
    import msvcrt


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
            str(TOOLS_DIR / "alacritty.exe"),
            "--config-file",
            str(TOOLS_DIR / "alacritty.toml"),
            "--command",
            sys.argv[0],
        ],
        env=env,
    )

    os._exit(0)


def get_version() -> str:
    return version("pvzrskintools")


def set_title(title: str) -> None:
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetConsoleTitleW(title)


def flush_input():
    if sys.platform == "win32":
        while msvcrt.kbhit():
            msvcrt.getch()
