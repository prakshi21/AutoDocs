from dataclasses import dataclass, field

from models.document_type import DocumentType


@dataclass(slots=True)
class RepositoryDocument:
    """
    Canonical document representation used throughout the AI pipeline.

    Every parser artifact is eventually converted into one of these.
    """

    id: str

    document_type: DocumentType

    title: str

    content: str

    metadata: dict[str, str] = field(default_factory=dict)
