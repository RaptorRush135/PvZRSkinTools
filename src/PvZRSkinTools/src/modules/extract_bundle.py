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

from src import asset_processor
from src import game_scanner
from src.file_dialog import FileDialog
from src.paths import BASE_DIR


def run(console: Console) -> None:
    dialog = FileDialog(console)

    bundle_path = game_scanner.pick_spine_bundle(dialog)

    default_output_directory = BASE_DIR / "output"

    output_directory = dialog.pick_directory(
        "Select an output directory",
        initial_directory=str(default_output_directory),
        must_be_empty=True,
        create_if_missing=True,
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
