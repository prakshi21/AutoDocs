from embeddings.embeddings_config import EmbeddingConfig
from embeddings.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)
from models.document_chunk import DocumentChunk


def test_generate_embedding():

    provider = SentenceTransformerEmbeddingProvider(
        config=EmbeddingConfig(),
    )

    chunk = DocumentChunk(
        id="chunk1",
        parent_document_id="doc1",
        chunk_index=0,
        content="Machine learning is amazing.",
    )

    embeddings = provider.embed_chunk([chunk])

    assert len(embeddings) == 1
    embedding = embeddings[0]

    assert embedding.chunk_id == "chunk1"

    assert len(embedding.vector) > 0

    assert isinstance(embedding.vector[0], float)
