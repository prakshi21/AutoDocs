from typing import Protocol

from llm.llm_response import LLMResponse


class LLMProvider(Protocol):
    """
    Interface for LLM providers.
    """

    def generate(
        self,
        question: str,
        context: str,
    ) -> LLMResponse:
        """
        Generate an answer using the supplied context.
        """
        ...
