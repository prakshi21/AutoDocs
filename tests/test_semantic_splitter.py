from chunking.semantic_splitter import SemanticSplitter
from models.document_type import DocumentType
from models.repository_document import RepositoryDocument


def test_split_documentation_into_paragraphs():
    document = RepositoryDocument(
        id="1",
        document_type=DocumentType.DOCUMENTATION,
        title="README",
        content=(
            "Section: Installation\n" "\n" "Run\n" "\n" "pip install\n" "\n" "Done"
        ),
    )

    splitter = SemanticSplitter()

    pieces = splitter.split(document)

    assert pieces == [
        "Section: Installation",
        "Run",
        "pip install",
        "Done",
    ]


def test_symbol_not_split():
    document = RepositoryDocument(
        id="1",
        document_type=DocumentType.SYMBOL,
        title="login",
        content="Name: login\nDocumentation:\nLogin user",
    )

    splitter = SemanticSplitter()

    pieces = splitter.split(document)

    assert len(pieces) == 1
    assert pieces[0] == document.content


def test_code_block_is_not_split():

    document = RepositoryDocument(
        id="1",
        document_type=DocumentType.DOCUMENTATION,
        title="README",
        content=(
            "Section: Installation\n"
            "\n"
            "```bash\n"
            "pip install\n"
            "\n"
            "pip install numpy\n"
            "```\n"
            "\n"
            "Done."
        ),
    )

    splitter = SemanticSplitter()

    pieces = splitter.split(document)

    assert len(pieces) == 3

    assert "pip install numpy" in pieces[1]


def test_empty_code_block():

    document = RepositoryDocument(
        id="1",
        document_type=DocumentType.DOCUMENTATION,
        title="README",
        content=("```\n" "```"),
    )

    splitter = SemanticSplitter()

    pieces = splitter.split(document)

    assert len(pieces) == 1


def test_multiple_code_blocks():

    document = RepositoryDocument(
        id="1",
        document_type=DocumentType.DOCUMENTATION,
        title="README",
        content=(
            "```python\n"
            "print(1)\n"
            "```\n"
            "\n"
            "Text\n"
            "\n"
            "```bash\n"
            "echo hello\n"
            "```"
        ),
    )

    splitter = SemanticSplitter()

    pieces = splitter.split(document)

    assert len(pieces) == 3


def test_heading_starts_new_piece():

    document = RepositoryDocument(
        id="1",
        document_type=DocumentType.DOCUMENTATION,
        title="README",
        content=("Intro\n" "\n" "# Installation\n" "Run\n" "\n" "# Usage\n" "Execute"),
    )

    splitter = SemanticSplitter()

    pieces = splitter.split(document)

    assert len(pieces) == 3

    assert pieces[0] == "Intro"

    assert pieces[1].startswith("# Installation")

    assert pieces[2].startswith("# Usage")
