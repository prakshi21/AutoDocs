from models.code_symbol import CodeSymbol
from analyzer.repository_index import RepositoryIndex

from healing.change_type import ChangeType
from healing.symbol_change import SymbolChange


class RepositoryChangeDetector:
    """
    Detects semantic changes between two repository snapshots.
    """

    def detect(
        self,
        old_index: RepositoryIndex,
        new_index: RepositoryIndex,
    ) -> list[SymbolChange]:
        """
        Compare two RepositoryIndex objects and return all detected changes.
        """

        old_lookup = self._build_lookup(old_index)
        new_lookup = self._build_lookup(new_index)

        changes: list[SymbolChange] = []

        changes.extend(
            self._detect_added(
                old_lookup,
                new_lookup,
            )
        )

        changes.extend(
            self._detect_removed(
                old_lookup,
                new_lookup,
            )
        )

        changes.extend(
            self._detect_modified(
                old_lookup,
                new_lookup,
            )
        )

        return changes

    def _build_lookup(
        self,
        repository_index: RepositoryIndex,
    ) -> dict[str, CodeSymbol]:
        """
        Build a lookup table of repository symbols.
        """

        lookup = {}

        for symbol in repository_index.all_symbols:
            key = f"{symbol.file_path}::{symbol.name}"
            lookup[key] = symbol

        return lookup

    def _detect_added(
        self,
        old_lookup: dict[str, CodeSymbol],
        new_lookup: dict[str, CodeSymbol],
    ) -> list[SymbolChange]:

        changes = []

        for key, symbol in new_lookup.items():

            if key not in old_lookup:

                changes.append(
                    SymbolChange(
                        symbol_name=symbol.name,
                        file_path=symbol.file_path,
                        change_type=ChangeType.ADDED,
                        new_signature=symbol.signature,
                        new_docstring=symbol.docstring,
                    )
                )

        return changes

    def _detect_removed(
        self,
        old_lookup: dict[str, CodeSymbol],
        new_lookup: dict[str, CodeSymbol],
    ) -> list[SymbolChange]:

        changes = []

        for key, symbol in old_lookup.items():

            if key not in new_lookup:

                changes.append(
                    SymbolChange(
                        symbol_name=symbol.name,
                        file_path=symbol.file_path,
                        change_type=ChangeType.REMOVED,
                        old_signature=symbol.signature,
                        old_docstring=symbol.docstring,
                    )
                )

        return changes

    def _detect_modified(
        self,
        old_lookup: dict[str, CodeSymbol],
        new_lookup: dict[str, CodeSymbol],
    ) -> list[SymbolChange]:

        changes = []

        for key, old_symbol in old_lookup.items():

            if key not in new_lookup:
                continue

            new_symbol = new_lookup[key]

            # Signature changed
            if old_symbol.signature != new_symbol.signature:

                changes.append(
                    SymbolChange(
                        symbol_name=old_symbol.name,
                        file_path=old_symbol.file_path,
                        change_type=ChangeType.SIGNATURE_CHANGED,
                        old_signature=old_symbol.signature,
                        new_signature=new_symbol.signature,
                    )
                )

            # Docstring changed
            elif old_symbol.docstring != new_symbol.docstring:

                changes.append(
                    SymbolChange(
                        symbol_name=old_symbol.name,
                        file_path=old_symbol.file_path,
                        change_type=ChangeType.DOCSTRING_CHANGED,
                        old_docstring=old_symbol.docstring,
                        new_docstring=new_symbol.docstring,
                    )
                )

        return changes
