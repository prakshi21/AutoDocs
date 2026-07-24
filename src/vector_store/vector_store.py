from typing import Protocol

from embeddings.embedding_collection import EmbeddingCollection
from models.embedding import Embedding


class VectorStore(Protocol):
    """
    Interface for vector databases.
    """

    def add(
        self,
        embeddings: EmbeddingCollection,
    ) -> None:
        """
        Store embeddings.
        """
        ...

    def search(
        self,
        query_embedding: list[float],
        k: int = 5,
    ) -> list[Embedding]:
        """
        Return the k most similar embeddings.
        """
        ...
