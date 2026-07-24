from models.embedding import Embedding


def test_create_embedding():

    embedding = Embedding(
        chunk_id="chunk1",
        vector=[1.0, 2.0, 3.0],
    )

    assert embedding.chunk_id == "chunk1"

    assert embedding.vector == [1.0, 2.0, 3.0]


def test_metadata_defaults_to_empty():

    embedding = Embedding(
        chunk_id="1",
        vector=[0.1],
    )

    assert embedding.metadata == {}
