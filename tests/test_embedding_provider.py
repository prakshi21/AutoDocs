from embeddings.embedding_provider import EmbeddingProvider
from models.document_chunk import DocumentChunk
from models.embedding import Embedding


class FakeEmbeddingProvider:
    def embed_documents(
        self,
        chunks: list[DocumentChunk],
    ) -> list[Embedding]:
        return [
            Embedding(
                chunk_id=chunk.id,
                vector=[1.0, 2.0, 3.0],
            )
            for chunk in chunks
        ]

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        return [1.0, 2.0, 3.0]


def test_fake_provider_implements_protocol():

    provider: EmbeddingProvider = FakeEmbeddingProvider()

    chunk = DocumentChunk(
        id="chunk1",
        parent_document_id="doc1",
        chunk_index=0,
        content="Hello",
    )

    embeddings = provider.embed_documents([chunk])

    assert len(embeddings) == 1
    assert embeddings[0].chunk_id == "chunk1"
    assert embeddings[0].vector == [1.0, 2.0, 3.0]

    query_vector = provider.embed_query("test query")
    assert query_vector == [1.0, 2.0, 3.0]
