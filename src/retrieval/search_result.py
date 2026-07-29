from dataclasses import dataclass, field


@dataclass(slots=True)
class SearchResult:
    """
    Represents a single vector search result.
    """

    chunk_id: str

    score: float

    metadata: dict[str, str] = field(default_factory=dict)
