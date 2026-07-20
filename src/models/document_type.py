from enum import StrEnum


class DocumentType(StrEnum):
    """
    Types of repository documents.
    """

    SYMBOL = "symbol"
    DOCUMENTATION = "documentation"
