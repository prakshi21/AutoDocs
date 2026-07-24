from dataclasses import dataclass, field


@dataclass(slots=True)
class Embedding:
    """
    Represents a vector embedding generated for a DocumentChunk.
    """

    chunk_id: str

    vector: list[float]

    metadata: dict[str, str] = field(default_factory=dict)
