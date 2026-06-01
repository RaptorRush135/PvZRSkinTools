from pathlib import Path
import time

from tkinter import Tk, filedialog

from rich.console import Console


class FileDialog:
    def __init__(self, console: Console):
        self.console = console
        self.root = Tk()
        self.root.withdraw()
        self.root.attributes("-topmost", True)  # type: ignore

    def pick_directory(
        self,
        title: str,
        initial_directory: str | None = None,
        must_be_empty: bool = False,
    ) -> Path:
        self.console.print(f"{title}:")

        while True:
            directory = filedialog.askdirectory(
                title=title, initialdir=initial_directory
            )

            if not directory:
                self.print_warning("No directory selected")
                continue

            path = Path(directory)
            if not path.exists():
                self.print_warning("Directory does not exist")
                continue

            if must_be_empty and any(path.iterdir()):
                self.print_warning("Directory must be empty")
                continue

            self.console.print(f"Selected: [dim]{path}[/dim]")
            return path

    def print_warning(self, message: str, delay: bool = True):
        self.console.print(f"[yellow]⚠  {message}[/yellow]")
        print("\a", end="")
        if delay:
            time.sleep(2)
