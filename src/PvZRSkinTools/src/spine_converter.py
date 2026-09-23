import subprocess
from enum import Enum, StrEnum
from pathlib import Path

from SpineAtlas import ReadAtlasFile  # pyright: ignore[reportMissingTypeStubs]

from src.paths import TOOLS_DIR


def __get_exe(name: str) -> str:
    return str(TOOLS_DIR / f"{name}.exe")


CONVERTER_EXE = __get_exe("SpineSkeletonDataConverter")


class SpineVersion(Enum):
    V3 = 3
    V4 = 4


class SkeletonFormat(StrEnum):
    SKEL = "skel"
    JSON = "json"


def get_version_string(version: SpineVersion) -> str:
    match version:
        case SpineVersion.V3:
            return "3.8.0"
        case SpineVersion.V4:
            return "4.2.0"


def convert_skeleton(
    input_file: Path,
    output_file: Path,
    version: SpineVersion | None = None,
) -> str | None:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    command = [CONVERTER_EXE, str(input_file), str(output_file)]
    if version is not None:
        command.extend(["-v", get_version_string(version)])

    try:
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        return f"Converter executable not found: '{CONVERTER_EXE}'"
    except subprocess.CalledProcessError as ex:
        stderr = ex.stderr.strip()
        if stderr:
            return stderr

        return f"Converter exited with code {ex.returncode}"

    return None


def convert_atlas(
    input_file: Path,
    output_file: Path,
    version: SpineVersion,
) -> None:
    atlas = ReadAtlasFile(input_file)
    atlas.version = version == SpineVersion.V4
    atlas.SaveAtlas(output_file)
