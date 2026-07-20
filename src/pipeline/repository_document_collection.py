from collections.abc import Iterator

from models.document_type import DocumentType
from models.repository_document import RepositoryDocument


class RepositoryDocumentCollection:
    """
    Collection of RepositoryDocuments.

    Provides a unified interface for managing all repository
    documents before chunking and embedding.
    """

    def __init__(self) -> None:
        self._documents: list[RepositoryDocument] = []

    def add(
        self,
        document: RepositoryDocument,
    ) -> None:
        """
        Add a document to the collection.
        """
        self._documents.append(document)

    @property
    def documents(self) -> list[RepositoryDocument]:
        """
        Return all repository documents.
        """
        return self._documents

    @property
    def count(self) -> int:
        """
        Total number of documents.
        """
        return len(self._documents)

    def by_type(
        self,
        document_type: DocumentType,
    ) -> list[RepositoryDocument]:
        """
        Return all documents of a given type.
        """
        return [
            document
            for document in self._documents
            if document.document_type == document_type
        ]

    def find(
        self,
        document_id: str,
    ) -> RepositoryDocument | None:
        """
        Find a document by ID.
        """
        for document in self._documents:
            if document.id == document_id:
                return document

        return None

    def __iter__(self) -> Iterator[RepositoryDocument]:
        return iter(self._documents)

    def __len__(self) -> int:
        return len(self._documents)
