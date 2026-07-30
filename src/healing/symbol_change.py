from dataclasses import dataclass

from healing.change_type import ChangeType


@dataclass(slots=True)
class SymbolChange:
    """
    Represents a single change detected
    in a repository symbol.
    """

    symbol_name: str

    file_path: str

    change_type: ChangeType

    old_signature: str | None = None

    new_signature: str | None = None

    old_docstring: str | None = None

    new_docstring: str | None = None
