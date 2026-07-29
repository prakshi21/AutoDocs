from models.document_chunk import DocumentChunk
from retrieval.context_builder import ContextBuilder
from retrieval.retrieved_chunk import RetrievedChunk


def test_build_context():

    chunk = DocumentChunk(
        id="chunk1",
        parent_document_id="doc1",
        chunk_index=0,
        content="JWT authentication is implemented using tokens.",
        metadata={
            "file_path": "auth.py",
        },
    )

    retrieved = RetrievedChunk(
        chunk=chunk,
        score=0.95,
    )

    builder = ContextBuilder()

    context = builder([retrieved])

    assert "JWT authentication" in context
    assert "auth.py" in context
