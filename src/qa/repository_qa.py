from llm.llm_provider import LLMProvider
from retrieval.context_builder import ContextBuilder
from retrieval.query_embedder import QueryEmbedder
from retrieval.retriever import Retriever


class RepositoryQA:
    """
    High-level orchestrator for repository question answering.
    """

    def __init__(
        self,
        query_embedder: QueryEmbedder,
        retriever: Retriever,
        context_builder: ContextBuilder,
        llm: LLMProvider,
    ) -> None:

        self._query_embedder = query_embedder
        self._retriever = retriever
        self._context_builder = context_builder
        self._llm = llm

    def ask(
        self,
        question: str,
    ):
        """
        Answer a question about the indexed repository.
        """

        query_embedding = self._query_embedder.embed(question)

        retrieved_chunks = self._retriever.retrieve(query_embedding)

        context = self._context_builder.build(retrieved_chunks)

        return self._llm.generate(
            question=question,
            context=context,
        )
