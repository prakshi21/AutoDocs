import chromadb

from chromadb.config import Settings

from embeddings.embedding_collection import EmbeddingCollection
from models.embedding import Embedding
from vector_store.chroma_config import ChromaConfig
from vector_store.vector_store import VectorStore


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
        metadatas = (
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
    ) -> list[Embedding]:
        """
        Search for the most similar embeddings.
        """

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=[
                "embeddings",
                "metadatas",
            ],
        )

        ids = results.get("ids")
        if not ids or not ids[0]:
            return []

        vectors = results.get("embeddings")
        metadatas = results.get("metadatas")

        ids_list = ids[0]
        vectors_list = vectors[0] if vectors is not None else [[]] * len(ids_list)
        metadatas_list = (
            metadatas[0] if metadatas is not None else [None] * len(ids_list)
        )

        embeddings: list[Embedding] = []
        for chunk_id, vector, metadata in zip(
            ids_list,
            vectors_list,
            metadatas_list,
        ):
            clean_metadata: dict[str, str] = {}
            if metadata is not None:
                clean_metadata = {
                    k: str(v)
                    for k, v in metadata.items()
                    if k != "_placeholder" and v is not None
                }

            embeddings.append(
                Embedding(
                    chunk_id=chunk_id,
                    vector=vector,
                    metadata=clean_metadata,
                )
            )

        return embeddings
