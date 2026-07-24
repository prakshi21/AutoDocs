from embeddings.embedding_collection import EmbeddingCollection
from models.embedding import Embedding
from vector_store.chroma_config import ChromaConfig
from vector_store.chroma_vector_store import ChromaVectorStore

config = ChromaConfig()

store = ChromaVectorStore(config)

embeddings = EmbeddingCollection()
embeddings.add(
    Embedding(
        chunk_id="chunk1",
        vector=[1.0, 0.0, 0.0],
    )
)
embeddings.add(
    Embedding(
        chunk_id="chunk2",
        vector=[0.0, 1.0, 0.0],
    )
)

store.add(embeddings)

query = embeddings.embeddings[0].vector

results = store.search(
    query,
    k=3,
)

for embedding in results:
    print(embedding.chunk_id)
