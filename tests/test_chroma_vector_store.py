from embeddings.embedding_collection import EmbeddingCollection
from models.embedding import Embedding
from vector_store.chroma_config import ChromaConfig
from vector_store.chroma_vector_store import ChromaVectorStore


def test_add_and_search(tmp_path):

    config = ChromaConfig(
        persist_directory=str(tmp_path),
        collection_name="test",
    )

    store = ChromaVectorStore(config)

    collection = EmbeddingCollection()

    collection.add(
        Embedding(
            chunk_id="chunk1",
            vector=[1.0, 0.0],
        )
    )

    collection.add(
        Embedding(
            chunk_id="chunk2",
            vector=[0.0, 1.0],
        )
    )

    store.add(collection)

    results = store.search(
        [1.0, 0.0],
        k=1,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk1"
