import chromadb

from chromadb.config import Settings

from embeddings.embedding_collection import EmbeddingCollection
from vector_store.chroma_config import ChromaConfig
from vector_store.vector_store import VectorStore
from retrieval.search_result import SearchResult


class ChromaVectorStore(VectorStore):
    """
    Vector store backed by ChromaDB.
    """

    def __init__(
        self,
        config: ChromaConfig,
    ) -> None:

        self._config = config

        self._client = chromadb.PersistentClient(
            path=config.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
            ),
        )

        self._collection = self._client.get_or_create_collection(
            name=config.collection_name,
            metadata={
                "hnsw:space": config.distance_function,
            },
        )

    def add(
        self,
        embeddings: EmbeddingCollection,
    ) -> None:
        """
        Store embeddings in ChromaDB.
        """

        if len(embeddings) == 0:
            return

        has_non_empty = any(len(embedding.metadata) > 0 for embedding in embeddings)
        metadatas: chromadb.Metadatas | None = (
            [
                (
                    embedding.metadata
                    if len(embedding.metadata) > 0
                    else {"_placeholder": "true"}
                )
                for embedding in embeddings
            ]
            if has_non_empty
            else None
        )

        self._collection.add(
            ids=[embedding.chunk_id for embedding in embeddings],
            embeddings=[embedding.vector for embedding in embeddings],
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        k: int = 5,
    ) -> list[SearchResult]:

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=[
                "distances",
                "metadatas",
            ],
        )

        ids = results["ids"][0] if results["ids"] is not None else []
        distances = results["distances"][0] if results["distances"] is not None else []
        metadatas = results["metadatas"][0] if results["metadatas"] is not None else []

        search_results: list[SearchResult] = []

        for chunk_id, distance, metadata in zip(
            ids,
            distances,
            metadatas,
        ):
            search_results.append(
                SearchResult(
                    chunk_id=chunk_id,
                    score=1.0 - float(distance),
                    metadata={k: str(v) for k, v in metadata.items()} if metadata else {},
                )
            )

        return search_results

