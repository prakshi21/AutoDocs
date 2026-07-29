from embeddings.embedding_provider import EmbeddingProvider


class QueryEmbedder:
    """
    Converts natural language queries into vector embeddings.
    """

    def __init__(
        self,
        provider: EmbeddingProvider,
    ) -> None:
        self._provider = provider

    def embed(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate an embedding for a query.
        """

        return self._provider.embed_query(query)
