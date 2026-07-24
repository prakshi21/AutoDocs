from sentence_transformers import SentenceTransformer
from embeddings.embeddings_config import EmbeddingConfig
from embeddings.embedding_provider import EmbeddingProvider
from models.document_chunk import DocumentChunk
from models.embedding import Embedding


class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    """
    Embedding provider backed by a SentenceTransformer model.
    """

    def __init__(
        self,
        config: EmbeddingConfig,
    ) -> None:
        self._config = config
        self._model = SentenceTransformer(config.model_name)

    def embed_chunk(
        self,
        chunks: list[DocumentChunk],
    ) -> list[Embedding]:
        """
        Generate an embedding for a document chunk.
        """

        vectors = self._model.encode(
            [chunk.content for chunk in chunks],
            convert_to_numpy=True,
        )

        embeddings: list[Embedding] = []

        for chunk, vector in zip(chunks, vectors):
            embeddings.append(
                Embedding(
                    chunk_id=chunk.id,
                    vector=vector.tolist(),
                    metadata=chunk.metadata.copy(),
                )
            )

        return embeddings
