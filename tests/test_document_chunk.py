from models.document_chunk import DocumentChunk


def test_create_chunk():

    chunk = DocumentChunk(
        id="chunk1",
        parent_document_id="doc1",
        chunk_index=0,
        content="hello",
    )

    assert chunk.id == "chunk1"
    assert chunk.parent_document_id == "doc1"
    assert chunk.chunk_index == 0
    assert chunk.content == "hello"


def test_metadata_defaults_to_empty():

    chunk = DocumentChunk(
        id="1",
        parent_document_id="2",
        chunk_index=0,
        content="abc",
    )

    assert chunk.metadata == {}
