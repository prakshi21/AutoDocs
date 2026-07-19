from models.code_symbol import CodeSymbol
from models.document_section import DocumentSection
from analyser.repository_index import RepositoryIndex


class RepositoryIndexer:
    """
    Builds a RepositoryIndex from parsed repository artifacts.
    """

    def build(
        self,
        symbols: list[CodeSymbol],
        documents: list[DocumentSection],
    ) -> RepositoryIndex:
        """
        Build and return a RepositoryIndex.

        Args:
            symbols: Parsed Python symbols.
            documents: Parsed Markdown sections.

        Returns:
            A populated RepositoryIndex.
        """

        index = RepositoryIndex()

        for symbol in symbols:
            index.add_symbol(symbol)

        for document in documents:
            index.add_document(document)

        return index
