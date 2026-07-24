from embeddings.embedding_generator import EmbeddingGenerator
from models.document_chunk import DocumentChunk
from models.embedding import Embedding
from pipeline.document_chunk_collection import DocumentChunkCollection


class FakeEmbeddingProvider:
    def embed_chunk(
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


def test_generate_embeddings():

    chunks = DocumentChunkCollection()

    chunks.add(
        DocumentChunk(
            id="chunk1",
            parent_document_id="doc1",
            chunk_index=0,
            content="Hello",
        )
    )

    chunks.add(
        DocumentChunk(
            id="chunk2",
            parent_document_id="doc1",
            chunk_index=1,
            content="World",
        )
    )

    generator = EmbeddingGenerator(
        provider=FakeEmbeddingProvider(),
    )

    embeddings = generator.generate(chunks)

    assert len(embeddings) == 2

    assert embeddings.embeddings[0].chunk_id == "chunk1"
    assert embeddings.embeddings[1].chunk_id == "chunk2"
