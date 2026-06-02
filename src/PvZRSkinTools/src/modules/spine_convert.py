from pathlib import Path
import shlex
from typing import Callable, Optional

from rich.console import Console

from src import choice_picker
from src.choice_picker import Choice

from src import spine_converter
from src.spine_converter import SpineVersion
from src.spine_converter import SkeletonFormat


def run(console: Console) -> None:
    version: Optional[SpineVersion] = choice_picker.prompt(
        message="Pick output Spine Version:",
        choices=[
            Choice(value=None, name="Keep (use input version)"),
            Choice(value=SpineVersion.V3, name="V3"),
            Choice(value=SpineVersion.V4, name="V4"),
        ],
    )

    skel_choices: list[Choice[Optional[SkeletonFormat]]] = [
        Choice(value=None, name="Keep (same as input)"),
        Choice(value=SkeletonFormat.SKEL, name=SkeletonFormat.SKEL.value),
        Choice(value=SkeletonFormat.JSON, name=SkeletonFormat.JSON.value),
    ]

    if version is None:
        skel_choices.pop(0)

    skel_format = choice_picker.prompt(
        message="Pick skeleton output format:",
        choices=skel_choices,
    )

    while True:
        raw_paths = __read_paths(console)
        if len(raw_paths) == 0:
            return

        paths = __resolve_paths(raw_paths)
        console.print(f"Resolved {len(paths)} file(s) to process:")
        for path in paths:
            console.print(f"[dim]{path}")

        __process_paths(console, paths, version, skel_format)


def __read_paths(console: Console) -> list[Path]:
    console.print(
        "Drag & drop files into this terminal and press Enter "
        "(or leave empty to go back):"
    )

    line = input().strip()

    if not line:
        return []

    return [Path(token.strip('"')) for token in shlex.split(line, posix=False)]


def __resolve_paths(paths: list[Path]) -> list[Path]:
    max_resolve_depth = 2
    seen: set[Path] = set()
    resolved: list[Path] = []

    def add_file(file: Path) -> None:
        if file in seen or file.suffix.lower() not in {".skel", ".json", ".atlas"}:
            return

        seen.add(file)
        resolved.append(file)

    def visit(path: Path, depth: int) -> None:
        if path.is_file():
            add_file(path)
            return

        if not path.is_dir() or depth > max_resolve_depth:
            return

        for child in path.iterdir():
            visit(child, depth + 1)

    for path in paths:
        visit(path, 0)

    return resolved


def __process_paths(
    console: Console,
    paths: list[Path],
    version: SpineVersion | None,
    skel_format: SkeletonFormat | None,
):
    def print_success() -> None:
        console.print("[bold green] ✓ Converted\n")

    def print_warning(message: str) -> None:
        console.print(f"[yellow]⚠  {message}\n")

    print()

    if not paths:
        print_warning("No files provided, aborting.")
        return

    for path in paths:
        console.print(f"Processing: [dim]{path}")
        if not path.exists():
            print_warning("Path does not exist!")
            continue

        suffix = path.suffix.lower()
        try:
            if suffix != ".atlas":
                out_path = __validate_output_path(
                    __try_get_output_path(path, version, skel_format),
                    print_warning,
                )
                if out_path is None:
                    continue

                console.print(f" - Converting skeleton: {path.name} -> {out_path.name}")
                error = spine_converter.convert_skeleton(path, out_path, version)
                if error is None:
                    print_success()
                else:
                    console.print(f" [red]{error}\n")
            else:
                out_path = __validate_output_path(
                    __try_get_output_path(path, version), print_warning
                )
                if out_path is None:
                    continue

                assert version is not None
                console.print(f" - Converting atlas: {path.name} -> {out_path.name}")
                spine_converter.convert_atlas(path, out_path, version)
                print_success()
        except Exception:  # pylint: disable=broad-exception-caught
            console.print_exception()
            console.print()

    console.print("[bold green]✓ Done!\n")


def __try_get_output_path(
    path: Path, version: SpineVersion | None, skel_format: SkeletonFormat | None = None
) -> Path | None:
    current_format = path.suffix.removeprefix(".")

    if version is None and (skel_format is None or skel_format.value == current_format):
        return None

    extension = f".{skel_format.value}" if skel_format is not None else path.suffix

    name_suffix = f"_v{version.value}" if version is not None else "_new"

    return path.with_name(f"{path.stem}{name_suffix}{extension}")


def __validate_output_path(
    out_path: Path | None, print_warning: Callable[[str], None]
) -> Path | None:
    if out_path is None:
        print_warning("Skipping: No conversion!")
        return None
    if out_path.exists():
        print_warning(f"Skipping: Output file already exists ({out_path.name})")
        return None

    return out_path
