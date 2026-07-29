from dataclasses import dataclass


@dataclass(slots=True)
class ContextConfig:
    """
    Configuration for building LLM context.
    """

    max_chunks: int = 5

    include_metadata: bool = True

    separator: str = "\n\n" + "=" * 80 + "\n\n"
