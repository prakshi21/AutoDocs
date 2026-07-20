from pipeline.document_builder import RepositoryDocumentBuilder

from models.document_section import DocumentSection
from models.document_type import DocumentType
from models.code_symbol import CodeSymbol
from models.enums import SymbolType


def test_build_documentation_document():
    section = DocumentSection(
        id="README::Installation",
        title="Installation",
        content="pip install",
        file_path="README.md",
        level=2,
        start_line=10,
        end_line=15,
    )

    builder = RepositoryDocumentBuilder()

    document = builder._build_documentation(section)

    assert document.document_type == DocumentType.DOCUMENTATION
    assert document.title == "Installation"
    assert "pip install" in document.content
    assert document.metadata["file_path"] == "README.md"


def test_build_symbol_document():

    symbol = CodeSymbol(
        id="auth.py::login",
        name="login",
        symbol_type=SymbolType.FUNCTION,
        file_path="auth.py",
        start_line=1,
        end_line=5,
        signature="login(email, password)",
        docstring="Authenticate user",
    )

    builder = RepositoryDocumentBuilder()

    document = builder._build_symbol(symbol)

    assert document.document_type == DocumentType.SYMBOL
    assert "Authenticate user" in document.content
    assert "login(email, password)" in document.content


def test_build():
    from analyzer.repository_index import RepositoryIndex

    index = RepositoryIndex()
    section = DocumentSection(
        id="README::Installation",
        title="Installation",
        content="pip install",
        file_path="README.md",
        level=2,
        start_line=10,
        end_line=15,
    )
    symbol = CodeSymbol(
        id="auth.py::login",
        name="login",
        symbol_type=SymbolType.FUNCTION,
        file_path="auth.py",
        start_line=1,
        end_line=5,
        signature="login(email, password)",
        docstring="Authenticate user",
    )
    index.add_document(section)
    index.add_symbol(symbol)

    builder = RepositoryDocumentBuilder()
    documents = builder.build(index)

    assert len(documents) == 2
    types = {doc.document_type for doc in documents}
    assert DocumentType.DOCUMENTATION in types
    assert DocumentType.SYMBOL in types
