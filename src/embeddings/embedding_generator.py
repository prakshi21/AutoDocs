from embeddings.embedding_collection import EmbeddingCollection
from embeddings.embedding_provider import EmbeddingProvider
from pipeline.document_chunk_collection import DocumentChunkCollection


class EmbeddingGenerator:
    """
    Generates embeddings for document chunks.
    """

    def __init__(
        self,
        provider: EmbeddingProvider,
    ) -> None:
        self._provider = provider

    def generate(
        self,
        chunks: DocumentChunkCollection,
    ) -> EmbeddingCollection:
        """
        Generate embeddings for all document chunks.
        """

        embedding_list = self._provider.embed_documents(list(chunks))

        collection = EmbeddingCollection()

        for embedding in embedding_list:
            collection.add(embedding)

        return collection
