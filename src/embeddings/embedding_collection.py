from collections.abc import Iterator

from models.embedding import Embedding


class EmbeddingCollection:
    """
    Collection of Embedding objects.
    """

    def __init__(self) -> None:
        self._embeddings: list[Embedding] = []

    def add(
        self,
        embedding: Embedding,
    ) -> None:
        """
        Add an embedding to the collection.
        """
        self._embeddings.append(embedding)

    @property
    def embeddings(self) -> list[Embedding]:
        """
        Return all embeddings.
        """
        return self._embeddings

    @property
    def count(self) -> int:
        """
        Return the number of embeddings.
        """
        return len(self._embeddings)

    def __len__(self) -> int:
        return len(self._embeddings)

    def __iter__(self) -> Iterator[Embedding]:
        return iter(self._embeddings)
