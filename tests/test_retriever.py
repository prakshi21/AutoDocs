from embeddings.embedding_collection import EmbeddingCollection
from models.document_chunk import DocumentChunk
from models.embedding import Embedding
from pipeline.document_chunk_collection import DocumentChunkCollection
from retrieval.retriever import Retriever
from retrieval.search_result import SearchResult


class FakeVectorStore:
    def __init__(self):
        self._results = []

    def add(self, embeddings: EmbeddingCollection):
        self._results.extend(embeddings)

    def search(self, query_embedding, k=5):
        return [
            SearchResult(
                chunk_id=embedding.chunk_id,
                score=1.0,
                metadata=embedding.metadata,
            )
            for embedding in self._results[:k]
        ]


def test_retrieve_chunks():

    chunks = DocumentChunkCollection()

    chunk = DocumentChunk(
        id="chunk1",
        parent_document_id="doc1",
        chunk_index=0,
        content="Authentication using JWT",
    )

    chunks.add(chunk)

    embeddings = EmbeddingCollection()

    embeddings.add(
        Embedding(
            chunk_id="chunk1",
            vector=[1.0, 2.0],
        )
    )

    store = FakeVectorStore()
    store.add(embeddings)

    retriever = Retriever(
        vector_store=store,
        chunks=chunks,
    )

    results = retriever.retrieve([1.0, 2.0])

    assert len(results) == 1
    assert results[0].chunk.content == "Authentication using JWT"
