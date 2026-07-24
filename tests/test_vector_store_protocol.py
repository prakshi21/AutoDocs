from embeddings.embedding_collection import EmbeddingCollection
from models.embedding import Embedding
from vector_store.vector_store import VectorStore


class FakeVectorStore:
    def __init__(self):
        self._embeddings = []

    def add(
        self,
        embeddings: EmbeddingCollection,
    ) -> None:
        self._embeddings.extend(embeddings)

    def search(
        self,
        query_embedding: list[float],
        k: int = 5,
    ) -> list[Embedding]:
        return self._embeddings[:k]


def test_fake_vector_store():

    collection = EmbeddingCollection()

    collection.add(
        Embedding(
            chunk_id="1",
            vector=[1.0, 2.0],
        )
    )

    store: VectorStore = FakeVectorStore()

    store.add(collection)

    results = store.search([1.0, 2.0])

    assert len(results) == 1
    assert results[0].chunk_id == "1"
