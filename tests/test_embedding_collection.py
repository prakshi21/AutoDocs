from embeddings.embedding_collection import EmbeddingCollection
from models.embedding import Embedding


def test_add_embedding():

    collection = EmbeddingCollection()

    embedding = Embedding(
        chunk_id="chunk1",
        vector=[1.0, 2.0],
    )

    collection.add(embedding)

    assert collection.count == 1
    assert len(collection) == 1
    assert collection.embeddings[0] == embedding


def test_collection_is_iterable():

    collection = EmbeddingCollection()

    collection.add(
        Embedding(
            chunk_id="1",
            vector=[1.0],
        )
    )

    collection.add(
        Embedding(
            chunk_id="2",
            vector=[2.0],
        )
    )

    chunk_ids = [embedding.chunk_id for embedding in collection]

    assert chunk_ids == ["1", "2"]


def test_empty_collection():

    collection = EmbeddingCollection()

    assert collection.count == 0
    assert len(collection) == 0
    assert list(collection) == []
