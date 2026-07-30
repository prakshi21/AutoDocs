from healing.change_type import ChangeType
from healing.symbol_change import SymbolChange


class DocumentationSearchQueryBuilder:
    """
    Builds semantic search queries for retrieving
    documentation related to a code change.
    """

    def build(
        self,
        change: SymbolChange,
    ) -> str:

        if change.change_type == ChangeType.ADDED:
            return f"Documentation describing " f"{change.symbol_name}"

        if change.change_type == ChangeType.REMOVED:
            return f"Documentation referencing " f"{change.symbol_name}"

        if change.change_type == ChangeType.SIGNATURE_CHANGED:
            return (
                f"Documentation describing "
                f"{change.symbol_name} "
                f"function parameters API usage"
            )

        if change.change_type == ChangeType.DOCSTRING_CHANGED:
            return f"Documentation explaining " f"{change.symbol_name}"

        return change.symbol_name
