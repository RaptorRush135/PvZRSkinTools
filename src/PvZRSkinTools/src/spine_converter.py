import subprocess
from enum import Enum
from pathlib import Path

from SpineAtlas import ReadAtlasFile  # pyright: ignore[reportMissingTypeStubs]

from paths import TOOLS_DIR


def __get_exe(name: str) -> str:
    return str(TOOLS_DIR / f"{name}.exe")


CONVERTER_EXE = __get_exe("SpineSkeletonDataConverter")


class AtlasVersion(Enum):
    V3 = 3
    V4 = 4


def convert_skeleton(
    input_file: Path,
    output_file: Path,
    version: str | None = None,
) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    command = [CONVERTER_EXE, str(input_file), str(output_file)]
    if version:
        command.extend(["-v", version])

    # TODO: Handle errors
    subprocess.run(command, stdout=subprocess.DEVNULL, check=True)


def convert_atlas(
    input_file: Path,
    output_file: Path,
    version: AtlasVersion,
) -> None:
    atlas = ReadAtlasFile(input_file)
    atlas.version = version == AtlasVersion.V4
    atlas.SaveAtlas(output_file)
