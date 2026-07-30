from unittest.mock import MagicMock

from healing.change_type import ChangeType
from healing.documentation_rewriter import DocumentationRewriter
from healing.symbol_change import SymbolChange
from llm.llm_response import LLMResponse
from models.document_chunk import DocumentChunk


def test_rewriter_calls_llm():

    llm = MagicMock()

    llm.generate.return_value = LLMResponse(answer="Updated documentation")

    rewriter = DocumentationRewriter(llm)

    change = SymbolChange(
        symbol_name="login",
        file_path="auth.py",
        change_type=ChangeType.SIGNATURE_CHANGED,
    )

    docs = [
        DocumentChunk(
            id="doc_chunk_1",
            parent_document_id="doc_1",
            chunk_index=0,
            content="Old documentation",
        )
    ]

    code = [
        DocumentChunk(
            id="code_chunk_1",
            parent_document_id="code_1",
            chunk_index=0,
            content="def login(email, password):",
        )
    ]

    result = rewriter.rewrite(
        change,
        docs,
        code,
    )

    llm.generate.assert_called_once()

    assert result == "Updated documentation"
