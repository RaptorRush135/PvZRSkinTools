import time

from rich.console import Console

from src import launcher

from src import choice_picker
from src.choice_picker import Choice

from src.modules import extract_bundle
from src.modules import guid_generator
from src.modules import spine_convert


console = Console()


def main() -> int:
    try:
        menu()
    except KeyboardInterrupt:
        console.print("\nCancelled...")
        return 130
    except Exception:  # pylint: disable=broad-exception-caught
        console.print_exception(show_locals=True)
        return 1
    return 0


def menu() -> None:
    while True:
        launcher.flush_input()
        choice = choice_picker.prompt(
            message="Pick an option:",
            choices=[
                Choice(value=1, name="1. Spine convert"),
                Choice(value=2, name="2. GUID generator"),
                Choice(value=3, name="3. Extract bundle"),
                Choice(value=4, name="4. Exit"),
            ],
        )

        try:
            should_exit = handle_options(choice)
            if should_exit:
                print()
                return
        except KeyboardInterrupt:
            print("\nCancelled...")
            time.sleep(1)

        print()


def handle_options(choice: int) -> bool:
    def show_cancel_msg():
        console.print("[dim]Press Ctrl+Shift+C to cancel a operation...[dim]\n")

    match choice:
        case 1:
            show_cancel_msg()
            spine_convert.run(console)
            return False
        case 2:
            show_cancel_msg()
            guid_generator.run(console)
            return False
        case 3:
            show_cancel_msg()
            extract_bundle.run(console)
            return False
        case _:
            return True


if __name__ == "__main__":
    launcher.ensure_relaunch()
    launcher.set_title(f"PvZRSkinTools v{launcher.get_version()}")
    EXIT_CODE = main()
    input("Press Enter to continue...")
    raise SystemExit(EXIT_CODE)
