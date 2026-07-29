from retrieval.context_config import ContextConfig
from retrieval.retrieved_chunk import RetrievedChunk


class ContextBuilder:
    """
    Builds the prompt context from retrieved chunks.
    """

    def __init__(
        self,
        config: ContextConfig | None = None,
    ) -> None:

        self._config = config or ContextConfig()

    def __call__(
        self,
        chunks: list[RetrievedChunk],
    ) -> str:
        return self.build(chunks)

    def build(
        self,
        chunks: list[RetrievedChunk],
    ) -> str:
        """
        Build the context sent to the LLM.
        """

        if not chunks:
            return ""

        sections: list[str] = []

        header = (
            "You are answering questions about a software repository.\n"
            "Use only the information provided below.\n"
        )

        for chunk in chunks[: self._config.max_chunks]:
            sections.append(self._format_chunk(chunk))

        return header + self._config.separator.join(sections)

    def _format_chunk(
        self,
        retrieved: RetrievedChunk,
    ) -> str:

        chunk = retrieved.chunk

        text: list[str] = []

        if self._config.include_metadata:

            text.append(f"File: {chunk.metadata.get('file_path', 'Unknown')}")

            text.append(f"Chunk ID: {chunk.id}")

            text.append(f"Score: {retrieved.score:.3f}")

            text.append("")

        text.append(chunk.content)

        return "\n".join(text)
