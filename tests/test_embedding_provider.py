from embeddings.embedding_provider import EmbeddingProvider
from models.document_chunk import DocumentChunk
from models.embedding import Embedding


class FakeEmbeddingProvider:
    def embed_chunk(
        self,
        chunk: DocumentChunk,
    ) -> Embedding:
        return Embedding(
            chunk_id=chunk.id,
            vector=[1.0, 2.0, 3.0],
        )


def test_fake_provider_implements_protocol():

    provider: EmbeddingProvider = FakeEmbeddingProvider()

    chunk = DocumentChunk(
        id="chunk1",
        parent_document_id="doc1",
        chunk_index=0,
        content="Hello",
    )

    embedding = provider.embed_chunk(chunk)

    assert embedding.chunk_id == "chunk1"

    assert embedding.vector == [1.0, 2.0, 3.0]
