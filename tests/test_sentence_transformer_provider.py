from unittest.mock import MagicMock, patch
import numpy as np

from embeddings.embeddings_config import EmbeddingConfig
from embeddings.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)
from models.document_chunk import DocumentChunk


def test_generate_embedding():
    mock_model = MagicMock()

    def mock_encode(sentences, convert_to_numpy=True):
        if isinstance(sentences, str):
            return np.array([0.1, 0.2, 0.3])
        return np.array([[0.1, 0.2, 0.3] for _ in sentences])

    mock_model.encode.side_effect = mock_encode

    with patch(
        "embeddings.sentence_transformer_provider.SentenceTransformer",
        return_value=mock_model,
    ):
        provider = SentenceTransformerEmbeddingProvider(
            config=EmbeddingConfig(),
        )

        chunk = DocumentChunk(
            id="chunk1",
            parent_document_id="doc1",
            chunk_index=0,
            content="Machine learning is amazing.",
        )

        embeddings = provider.embed_documents([chunk])

        assert len(embeddings) == 1
        embedding = embeddings[0]

        assert embedding.chunk_id == "chunk1"
        assert len(embedding.vector) == 3
        assert embedding.vector == [0.1, 0.2, 0.3]
        assert isinstance(embedding.vector[0], float)

        # Verify that embed_query also works correctly
        query_vector = provider.embed_query("test query")
        assert query_vector == [0.1, 0.2, 0.3]
