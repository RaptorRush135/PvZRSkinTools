from dataclasses import dataclass

from InquirerPy import inquirer
from InquirerPy.base.control import Choice as InquirerChoice


@dataclass(frozen=True)
class Choice[T]:
    value: T
    name: str | None = None

    def to_inquirer(self) -> InquirerChoice:
        return InquirerChoice(value=self.value, name=self.name)


def prompt[T](message: str, choices: list[Choice[T]]) -> T:
    return inquirer.select(  # pyright: ignore[reportPrivateImportUsage]
        message=message,
        choices=[choice.to_inquirer() for choice in choices],
    ).execute()
