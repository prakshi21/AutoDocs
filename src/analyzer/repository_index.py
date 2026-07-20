from dataclasses import dataclass, field

from models.code_symbol import CodeSymbol
from models.document_section import DocumentSection


@dataclass
class RepositoryIndex:

    symbols_by_file: dict[str, list[CodeSymbol]] = field(default_factory=dict)
    docs_by_file: dict[str, list[DocumentSection]] = field(default_factory=dict)

    symbol_lookup: dict[str, CodeSymbol] = field(default_factory=dict)
    document_lookup: dict[str, DocumentSection] = field(default_factory=dict)

    def add_symbol(self, symbol: CodeSymbol) -> None:
        """Add a code symbol to the index."""

        self.symbol_lookup[symbol.id] = symbol

        self.symbols_by_file.setdefault(symbol.file_path, []).append(symbol)

    def add_document(self, section: DocumentSection) -> None:
        """Add a markdown section to the index."""

        self.document_lookup[section.id] = section

        self.docs_by_file.setdefault(section.file_path, []).append(section)

    def get_symbol(self, symbol_id: str) -> CodeSymbol | None:
        """Return a symbol by its unique ID."""

        return self.symbol_lookup.get(symbol_id)

    def get_document(self, document_id: str) -> DocumentSection | None:
        """Return a document section by its unique ID."""

        return self.document_lookup.get(document_id)

    def get_symbols(self, file_path: str) -> list[CodeSymbol]:
        """Return all symbols belonging to a file."""

        return self.symbols_by_file.get(file_path, [])

    def get_documents(self, file_path: str) -> list[DocumentSection]:
        """Return all markdown sections belonging to a file."""

        return self.docs_by_file.get(file_path, [])

    @property
    def all_symbols(self) -> list[CodeSymbol]:
        """Return every indexed code symbol."""

        return list(self.symbol_lookup.values())

    @property
    def all_documents(self) -> list[DocumentSection]:
        """Return every indexed markdown section."""

        return list(self.document_lookup.values())

    @property
    def symbol_count(self) -> int:
        return len(self.symbol_lookup)

    @property
    def document_count(self) -> int:
        return len(self.document_lookup)
