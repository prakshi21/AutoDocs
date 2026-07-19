from dataclasses import dataclass


@dataclass
class ParsedArtifact:
    """
    Base class for all parsed repository artifacts.
    """

    id: str
    file_path: str
