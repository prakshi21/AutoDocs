from analyser.repository_index import RepositoryIndex
from analyser.repository_indexer import RepositoryIndexer
from parser.markdown_parser import MarkdownParser
from parser.python_parser import PythonParser


def test_build_repository_index():
    python_parser = PythonParser()
    markdown_parser = MarkdownParser()

    symbols = python_parser.parse("sample_repo/auth.py")
    documents = markdown_parser.parse("sample_repo/README.md")

    indexer = RepositoryIndexer()

    index = indexer.build(symbols, documents)

    assert isinstance(index, RepositoryIndex)

    assert index.symbol_count == 4
    assert index.document_count == 6


def test_lookup_symbol():
    python_parser = PythonParser()

    symbols = python_parser.parse("sample_repo/auth.py")

    index = RepositoryIndexer().build(symbols, [])

    login = index.get_symbol("sample_repo/auth.py::User.login")

    assert login is not None
    assert login.name == "User.login"


def test_lookup_document():
    markdown_parser = MarkdownParser()

    documents = markdown_parser.parse("sample_repo/README.md")

    index = RepositoryIndexer().build([], documents)

    installation = index.get_document("sample_repo/README.md::Installation")

    assert installation is not None
    assert installation.title == "Installation"


def test_get_symbols_by_file():
    python_parser = PythonParser()

    symbols = python_parser.parse("sample_repo/auth.py")

    index = RepositoryIndexer().build(symbols, [])

    assert len(index.get_symbols("sample_repo/auth.py")) == 4


def test_get_documents_by_file():
    markdown_parser = MarkdownParser()

    documents = markdown_parser.parse("sample_repo/README.md")

    index = RepositoryIndexer().build([], documents)

    assert len(index.get_documents("sample_repo/README.md")) == 6
