from typing import Protocol

from models.document_chunk import DocumentChunk
from models.embedding import Embedding


class EmbeddingProvider(Protocol):

    def embed_documents(
        self,
        chunks: list[DocumentChunk],
    ) -> list[Embedding]:
        """
        Generate embeddings for repository chunks.
        """
        ...

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate an embedding for a user query.
        """
        ...
