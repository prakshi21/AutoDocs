from models.document_type import DocumentType
from models.repository_document import RepositoryDocument


def test_create_repository_document():
    document = RepositoryDocument(
        id="auth.py::User.login",
        document_type=DocumentType.SYMBOL,
        title="User.login",
        content="Login user",
    )

    assert document.id == "auth.py::User.login"
    assert document.document_type == DocumentType.SYMBOL
    assert document.title == "User.login"
    assert document.content == "Login user"


def test_metadata_defaults_to_empty_dict():
    document = RepositoryDocument(
        id="1",
        document_type=DocumentType.DOCUMENTATION,
        title="README",
        content="Content",
    )

    assert document.metadata == {}


def test_metadata_can_be_supplied():
    document = RepositoryDocument(
        id="1",
        document_type=DocumentType.SYMBOL,
        title="add",
        content="Adds numbers",
        metadata={
            "language": "python",
        },
    )

    assert document.metadata["language"] == "python"
