from pipeline.document_chunk_collection import DocumentChunkCollection
from retrieval.retrieved_chunk import RetrievedChunk
from vector_store.vector_store import VectorStore
from retrieval.search_result import SearchResult


class Retriever:
    """
    Retrieves the most relevant document chunks.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        chunks: DocumentChunkCollection,
    ) -> None:

        self._vector_store = vector_store
        self._chunks = chunks

    def retrieve(
        self,
        query_embedding: list[float],
        k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant document chunks.
        """

        search_results: list[SearchResult] = self._vector_store.search(
            query_embedding=query_embedding,
            k=k,
        )

        retrieved: list[RetrievedChunk] = []

        for result in search_results:

            chunk = self._chunks.get_by_id(result.chunk_id)

            if chunk is None:
                continue

            retrieved.append(
                RetrievedChunk(
                    chunk=chunk,
                    score=result.score,
                )
            )

        return retrieved
