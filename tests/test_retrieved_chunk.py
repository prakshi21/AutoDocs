from models.document_chunk import DocumentChunk
from retrieval.retrieved_chunk import RetrievedChunk


def test_create_retrieved_chunk():

    chunk = DocumentChunk(
        id="chunk1",
        parent_document_id="doc1",
        chunk_index=0,
        content="Hello World",
    )

    retrieved = RetrievedChunk(
        chunk=chunk,
        score=0.95,
    )

    assert retrieved.chunk == chunk
    assert retrieved.score == 0.95
