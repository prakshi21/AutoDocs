from chunking.chunking_config import ChunkingConfig
from chunking.repository_chunker import RepositoryChunker
from chunking.semantic_splitter import SemanticSplitter
from chunking.token_counter import ApproximateTokenCounter
from models.document_type import DocumentType
from models.repository_document import RepositoryDocument
from pipeline.repository_document_collection import RepositoryDocumentCollection


def test_chunk_single_document():

    documents = RepositoryDocumentCollection()

    documents.add(
        RepositoryDocument(
            id="doc1",
            title="README",
            document_type=DocumentType.DOCUMENTATION,
            content="Hello World",
        )
    )

    chunker = RepositoryChunker(
        semantic_splitter=SemanticSplitter(),
        token_counter=ApproximateTokenCounter(),
        config=ChunkingConfig(),
    )

    chunks = chunker.chunk(documents)

    assert len(chunks) == 1

    chunk = chunks.chunks[0]

    assert chunk.parent_document_id == "doc1"
    assert chunk.chunk_index == 0
    assert chunk.content == "Hello World"


def test_multiple_chunks_created():

    documents = RepositoryDocumentCollection()

    documents.add(
        RepositoryDocument(
            id="doc1",
            title="README",
            document_type=DocumentType.DOCUMENTATION,
            content="First\n\nSecond\n\nThird",
        )
    )

    chunker = RepositoryChunker(
        semantic_splitter=SemanticSplitter(),
        token_counter=ApproximateTokenCounter(),
        config=ChunkingConfig(),
    )

    chunks = chunker.chunk(documents)

    assert len(chunks) == 3

    assert chunks.chunks[0].chunk_index == 0
    assert chunks.chunks[1].chunk_index == 1
    assert chunks.chunks[2].chunk_index == 2
