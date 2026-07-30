from models.document_chunk import DocumentChunk
from healing.symbol_change import SymbolChange
from llm.llm_provider import LLMProvider


class DocumentationRewriter:
    """
    Uses the LLM to rewrite outdated documentation
    based on the latest source code.
    """

    def __init__(
        self,
        llm: LLMProvider,
    ):
        self._llm = llm

    def rewrite(
        self,
        change: SymbolChange,
        documentation_chunks: list[DocumentChunk],
        code_chunks: list[DocumentChunk],
    ) -> str:

        prompt = self._build_prompt(
            change,
            documentation_chunks,
            code_chunks,
        )

        response = self._llm.generate(
            question=prompt,
            context="",
        )

        return response.answer

    def _build_prompt(
        self,
        change: SymbolChange,
        documentation_chunks: list[DocumentChunk],
        code_chunks: list[DocumentChunk],
    ) -> str:

        documentation = "\n\n".join(chunk.content for chunk in documentation_chunks)

        code = "\n\n".join(chunk.content for chunk in code_chunks)

        return f"""
You are updating technical documentation.

A code change has been detected.

Changed symbol:
{change.symbol_name}

Current documentation:

{documentation}

Latest source code:

{code}

Instructions:

- Update ONLY the affected documentation.
- Preserve the existing writing style.
- Preserve markdown formatting.
- Do not invent APIs.
- Do not modify unrelated sections.
- Return only the updated markdown.
"""
