from models.document_chunk import DocumentChunk
from healing.change_type import ChangeType
from healing.symbol_change import SymbolChange
from retrieval.query_embedder import QueryEmbedder
from retrieval.retriever import Retriever


class DocumentationMapper:
    """
    Maps a code change to the documentation
    chunks that describe it.
    """

    def __init__(
        self,
        query_embedder: QueryEmbedder,
        retriever: Retriever,
    ):
        self._query_embedder = query_embedder
        self._retriever = retriever

    def map(
        self,
        change: SymbolChange,
    ) -> list[DocumentChunk]:

        query = self._build_query(change)

        embedding = self._query_embedder.embed(query)

        retrieved_chunks = self._retriever.retrieve(embedding)

        return [r.chunk for r in retrieved_chunks]

    def _build_query(
        self,
        change: SymbolChange,
    ) -> str:

        if change.change_type == ChangeType.ADDED:
            return f"Documentation describing {change.symbol_name}"

        if change.change_type == ChangeType.REMOVED:
            return f"Documentation referencing {change.symbol_name}"

        if change.change_type == ChangeType.SIGNATURE_CHANGED:
            return (
                f"Documentation describing "
                f"{change.symbol_name} "
                f"function parameters usage"
            )

        if change.change_type == ChangeType.DOCSTRING_CHANGED:
            return f"Documentation explaining {change.symbol_name}"

        return change.symbol_name
