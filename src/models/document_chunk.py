from dataclasses import dataclass, field


@dataclass(slots=True)
class DocumentChunk:
    """
    A chunk derived from a RepositoryDocument.

    Chunks are the unit that will later be embedded
    and stored in the vector database.
    """

    id: str

    parent_document_id: str

    chunk_index: int

    content: str

    metadata: dict[str, str] = field(default_factory=dict)
