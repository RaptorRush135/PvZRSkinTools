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


def main():
    output_directory = Path("output")
    bundle_path = r"C:\Program Files (x86)\Steam\steamapps\common\PVZ Replanted\Replanted_Data\StreamingAssets\aa\StandaloneWindows64\spineassets_assets_assets\art\characters\spine.bundle"

    console = Console()
    console.print("[bold cyan]Loading bundle...[/bold cyan]")
    env = UnityPy.load(bundle_path)

    assets = [
        (path, obj)
        for path, obj in env.container.items()
        if asset_processor.asset_filter(path)
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}", table_column=Column(width=25)),
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

    console.print(f"[bold green]✓ Done![/bold green] Extracted {len(assets)} assets to [dim]{output_directory}[/dim]")

if __name__ == "__main__":
    main()
