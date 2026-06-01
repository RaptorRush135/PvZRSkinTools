import sys
from pathlib import Path

import UnityPy

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)
from rich.console import Console
from rich.table import Column

import asset_processor
import game_scanner
from file_dialog import FileDialog


console = Console()


def main():
    dialog = FileDialog(console)

    bundle_path = game_scanner.pick_spine_bundle(dialog)

    base_dir = str(Path(sys.executable).parent)
    output_directory = dialog.pick_directory(
        "Select an output directory", initial_directory=base_dir, must_be_empty=True
    )

    console.print("[bold cyan]Loading bundle...[/bold cyan]")
    env = UnityPy.load(str(bundle_path))

    assets = [
        (path, obj)
        for path, obj in env.container.items()
        if asset_processor.asset_filter(path)
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn(
            "[progress.description]{task.description}", table_column=Column(width=25)
        ),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Extracting assets...", total=len(assets))

        for path, obj in assets:
            file_name = asset_processor.get_asset_file_name(Path(path))

            progress.update(task, description=f"[cyan]{file_name}")

            asset_processor.process_asset(output_directory, file_name, obj)

            progress.advance(task)

    console.print(
        f"[bold green]✓ Done![/bold green] Extracted {len(assets)} assets to "
        f"[dim]{output_directory}[/dim]"
    )


if __name__ == "__main__":
    exit_code = None
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled...")
        exit_code = 130
    except Exception:  # pylint: disable=broad-exception-caught
        console.print_exception(show_locals=True)
        exit_code = 1

    input("Press Enter to continue...")

    if exit_code is not None:
        sys.exit(exit_code)
