from retrieval.query_embedder import QueryEmbedder


class FakeProvider:
    def embed_documents(self, chunks):
        return []

    def embed_query(
        self,
        query: str,
    ):
        return [1.0, 2.0, 3.0]


def test_embed_query():

    embedder = QueryEmbedder(
        provider=FakeProvider(),
    )

    vector = embedder.embed("What is JWT?")

    assert vector == [1.0, 2.0, 3.0]
