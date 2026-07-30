import os

from google import genai

from llm.llm_config import LLMConfig
from llm.llm_provider import LLMProvider
from llm.llm_response import LLMResponse


class GeminiProvider(LLMProvider):
    def __init__(
        self,
        config: LLMConfig,
    ) -> None:

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self._client = genai.Client(api_key=api_key)
        self._config = config

    def _build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        return f"""You are an expert software engineer.

    Answer the user's question ONLY using the provided repository context.

    If the answer cannot be found in the context, clearly state that.

    Repository Context:
    {context}

    User Question:
    {question}
    """

    def generate(
        self,
        question: str,
        context: str,
    ) -> LLMResponse:
        """
        Generate an answer using the repository context.
        """

        prompt = self._build_prompt(
            question=question,
            context=context,
        )

        response = self._client.models.generate_content(
            model=self._config.model_name,
            contents=prompt,
        )

        answer = response.text or "No response generated."

        return LLMResponse(
            answer=answer,
            metadata={
                "model": self._config.model_name,
            },
        )
