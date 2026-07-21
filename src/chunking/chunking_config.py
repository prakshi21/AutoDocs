from dataclasses import dataclass


@dataclass(slots=True)
class ChunkingConfig:
    """
    Configuration for repository chunking.
    """

    max_tokens: int = 512

    chunk_overlap: int = 0

    preserve_headings: bool = True

    preserve_code_blocks: bool = True

    min_chunk_size: int = 0
