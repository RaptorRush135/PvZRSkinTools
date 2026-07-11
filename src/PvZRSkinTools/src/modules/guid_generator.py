import time
import random
import uuid

from rich.console import Console
from rich.live import Live

import pyperclip

from src.choice_picker import Choice, prompt


def run(console: Console) -> None:
    while True:
        guid = __animate_guid(console)

        while True:
            console.print()
            choice = prompt(
                message="What next?",
                choices=[
                    Choice(value=1, name="1. Generate another"),
                    Choice(value=2, name="2. Copy to clipboard"),
                    Choice(value=3, name="3. Go back"),
                ],
            )

            match choice:
                case 1:
                    break
                case 2:
                    pyperclip.copy(guid)
                    console.print("[green]GUID copied to clipboard.[/green]")
                case _:
                    return


def __animate_guid(console: Console) -> str:
    final = str(uuid.uuid4())

    with Live("", console=console, refresh_per_second=30) as live:
        for locked in range(len(final) + 1):
            chars: list[str] = []

            for i, c in enumerate(final):
                if c == "-":
                    chars.append("-")
                elif i < locked:
                    chars.append(c)
                else:
                    chars.append(random.choice("0123456789abcdef"))

            live.update(f"[bold green]GUID:[/bold green] [bold]{''.join(chars)}[/bold]")

            time.sleep(0.015)

    return final
