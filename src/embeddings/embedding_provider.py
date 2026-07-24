from typing import Protocol

from models.document_chunk import DocumentChunk
from models.embedding import Embedding


class EmbeddingProvider(Protocol):
    """
    Interface for embedding providers.
    """

    def embed_chunk(
        self,
        chunks: list[DocumentChunk],
    ) -> list[Embedding]:
        """
        Generate embeddings for multiple document chunks.
        """
        ...
