from unittest.mock import MagicMock

from healing.change_type import ChangeType
from healing.documentation_mapper import DocumentationMapper
from healing.symbol_change import SymbolChange


def test_mapper_calls_embedder_and_retriever():

    embedder = MagicMock()
    retriever = MagicMock()

    embedder.embed.return_value = [0.1, 0.2, 0.3]

    chunk1 = MagicMock()
    chunk2 = MagicMock()
    retriever.retrieve.return_value = [
        MagicMock(chunk=chunk1),
        MagicMock(chunk=chunk2),
    ]

    mapper = DocumentationMapper(
        embedder,
        retriever,
    )

    change = SymbolChange(
        symbol_name="login",
        file_path="auth.py",
        change_type=ChangeType.SIGNATURE_CHANGED,
    )

    result = mapper.map(change)

    embedder.embed.assert_called_once()

    retriever.retrieve.assert_called_once()

    assert result == [chunk1, chunk2]
