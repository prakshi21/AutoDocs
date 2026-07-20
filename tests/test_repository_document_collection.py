from models.document_type import DocumentType
from models.repository_document import RepositoryDocument

from pipeline.repository_document_collection import (
    RepositoryDocumentCollection,
)


def test_add_document():
    collection = RepositoryDocumentCollection()

    document = RepositoryDocument(
        id="1",
        document_type=DocumentType.SYMBOL,
        title="add",
        content="Adds numbers",
    )

    collection.add(document)

    assert collection.count == 1


def test_find_document():
    collection = RepositoryDocumentCollection()

    document = RepositoryDocument(
        id="abc",
        document_type=DocumentType.SYMBOL,
        title="login",
        content="Login",
    )

    collection.add(document)

    assert collection.find("abc") == document


def test_find_unknown_document():
    collection = RepositoryDocumentCollection()

    assert collection.find("missing") is None


def test_filter_by_type():
    collection = RepositoryDocumentCollection()

    collection.add(
        RepositoryDocument(
            id="1",
            document_type=DocumentType.SYMBOL,
            title="login",
            content="...",
        )
    )

    collection.add(
        RepositoryDocument(
            id="2",
            document_type=DocumentType.DOCUMENTATION,
            title="README",
            content="...",
        )
    )

    symbols = collection.by_type(DocumentType.SYMBOL)

    assert len(symbols) == 1
    assert symbols[0].title == "login"


def test_collection_is_iterable():
    collection = RepositoryDocumentCollection()

    collection.add(
        RepositoryDocument(
            id="1",
            document_type=DocumentType.SYMBOL,
            title="login",
            content="...",
        )
    )

    assert len(list(collection)) == 1
