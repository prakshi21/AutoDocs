from models.code_symbol import CodeSymbol
from models.document_section import DocumentSection
from models.document_type import DocumentType
from models.repository_document import RepositoryDocument
from analyzer.repository_index import RepositoryIndex
from pipeline.repository_document_collection import RepositoryDocumentCollection


class RepositoryDocumentBuilder:
    """
    Converts a RepositoryIndex into RepositoryDocuments.
    """

    def build(
        self,
        repository_index: RepositoryIndex,
    ) -> RepositoryDocumentCollection:
        """
        Build RepositoryDocuments from a RepositoryIndex.
        """

        collection = RepositoryDocumentCollection()

        for section in repository_index.all_documents:
            collection.add(self._build_documentation(section))

        for symbol in repository_index.all_symbols:
            collection.add(self._build_symbol(symbol))

        return collection

    def _build_documentation(
        self,
        section: DocumentSection,
    ) -> RepositoryDocument:
        """
        Convert a markdown section into a RepositoryDocument.
        """
        parts: list[str] = []

        parts.append(f"Section: {section.title}")
        parts.append("")
        parts.append(section.content)

        content = "\n".join(parts)

        return RepositoryDocument(
            id=section.id,
            document_type=DocumentType.DOCUMENTATION,
            title=section.title,
            content=content,
            metadata={
                "file_path": section.file_path,
                "level": str(section.level),
                "start_line": str(section.start_line),
                "end_line": str(section.end_line),
            },
        )

    def _build_symbol(
        self,
        symbol: CodeSymbol,
    ) -> RepositoryDocument:
        """
        Convert a CodeSymbol into a RepositoryDocument.
        """

        parts: list[str] = []

        parts.append(f"File: {symbol.file_path}")
        parts.append("")

        parts.append(f"Name: {symbol.name}")
        parts.append(f"Type: {symbol.symbol_type.value}")

        parts.append("")
        parts.append("Signature:")
        parts.append(symbol.signature)

        if symbol.docstring:
            parts.append("")
            parts.append("Documentation:")
            parts.append(symbol.docstring)

        content = "\n".join(parts)

        return RepositoryDocument(
            id=symbol.id,
            document_type=DocumentType.SYMBOL,
            title=symbol.name,
            content=content,
            metadata={
                "file_path": symbol.file_path,
                "symbol_name": symbol.name,
                "symbol_type": symbol.symbol_type.value,
                "start_line": str(symbol.start_line),
                "end_line": str(symbol.end_line),
            },
        )
