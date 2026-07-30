from enum import Enum


class ChangeType(str, Enum):
    """
    Represents the type of change detected
    between two versions of a repository.
    """

    ADDED = "added"

    REMOVED = "removed"

    SIGNATURE_CHANGED = "signature_changed"

    DOCSTRING_CHANGED = "docstring_changed"

    MODIFIED = "modified"
