from dataclasses import dataclass

from models.document_chunk import DocumentChunk


@dataclass(slots=True)
class RetrievedChunk:
    """
    Represents a retrieved document chunk and its similarity score.
    """

    chunk: DocumentChunk

    score: float
