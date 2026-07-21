from chunking.chunking_config import ChunkingConfig
from chunking.semantic_splitter import SemanticSplitter
from chunking.token_counter import TokenCounter
from models.document_chunk import DocumentChunk
from models.repository_document import RepositoryDocument
from pipeline.document_chunk_collection import DocumentChunkCollection
from pipeline.repository_document_collection import RepositoryDocumentCollection


class RepositoryChunker:
    """
    Converts RepositoryDocuments into DocumentChunks.
    """

    def __init__(
        self,
        semantic_splitter: SemanticSplitter,
        token_counter: TokenCounter,
        config: ChunkingConfig,
    ) -> None:
        self._semantic_splitter = semantic_splitter
        self._token_counter = token_counter
        self._config = config

    def chunk(
        self,
        documents: RepositoryDocumentCollection,
    ) -> DocumentChunkCollection:
        """
        Convert a collection of RepositoryDocuments into
        a collection of DocumentChunks.
        """

        chunks = DocumentChunkCollection()

        for document in documents:
            self._chunk_document(
                document,
                chunks,
            )

        return chunks

    def _chunk_document(
        self,
        document: RepositoryDocument,
        output: DocumentChunkCollection,
    ) -> None:
        """
        Chunk a single RepositoryDocument.
        """

        pieces = self._semantic_splitter.split(document)

        for index, piece in enumerate(pieces):

            token_count = self._token_counter.count(piece)

            if token_count > self._config.max_tokens:
                raise NotImplementedError(
                    "Token splitting has not been implemented yet."
                )

            chunk = self._create_chunk(
                document=document,
                piece=piece,
                chunk_index=index,
            )

            output.add(chunk)

    def _create_chunk(
        self,
        document: RepositoryDocument,
        piece: str,
        chunk_index: int,
    ) -> DocumentChunk:
        """
        Create a DocumentChunk from a semantic piece.
        """

        return DocumentChunk(
            id=f"{document.id}::chunk{chunk_index}",
            parent_document_id=document.id,
            chunk_index=chunk_index,
            content=piece,
            metadata=document.metadata.copy(),
        )
