from analyzer.repository_index import RepositoryIndex
from analyzer.repository_indexer import RepositoryIndexer
from parser.markdown_parser import MarkdownParser
from parser.parser_registry import ParserRegistry
from parser.python_parser import PythonParser
from parser.repository_walker import RepositoryWalker


def test_build_repository_index():
    walker = RepositoryWalker()
    registry = ParserRegistry()
    registry.register(PythonParser())
    registry.register(MarkdownParser())

    indexer = RepositoryIndexer(walker, registry)
    index = indexer.build("sample_repo")

    assert isinstance(index, RepositoryIndex)
    assert index.symbol_count == 4
    assert index.document_count == 6


def test_lookup_symbol():
    walker = RepositoryWalker()
    registry = ParserRegistry()
    registry.register(PythonParser())

    indexer = RepositoryIndexer(walker, registry)
    index = indexer.build("sample_repo")

    login = index.get_symbol("sample_repo/auth.py::User.login")

    assert login is not None
    assert login.name == "User.login"


def test_lookup_document():
    walker = RepositoryWalker()
    registry = ParserRegistry()
    registry.register(MarkdownParser())

    indexer = RepositoryIndexer(walker, registry)
    index = indexer.build("sample_repo")

    installation = index.get_document("sample_repo/README.md::Installation")

    assert installation is not None
    assert installation.title == "Installation"


def test_get_symbols_by_file():
    walker = RepositoryWalker()
    registry = ParserRegistry()
    registry.register(PythonParser())

    indexer = RepositoryIndexer(walker, registry)
    index = indexer.build("sample_repo")

    assert len(index.get_symbols("sample_repo/auth.py")) == 4


def test_get_documents_by_file():
    walker = RepositoryWalker()
    registry = ParserRegistry()
    registry.register(MarkdownParser())

    indexer = RepositoryIndexer(walker, registry)
    index = indexer.build("sample_repo")

    assert len(index.get_documents("sample_repo/README.md")) == 6
