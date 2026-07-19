from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseParser(ABC, Generic[T]):
    """
    Base class for all parsers.
    Every parser must implement parse().
    """

    @property
    @abstractmethod
    def supported_extensions(self) -> set[str]:
        """
        Return the set of file extensions supported by this parser.
        """
        pass

    @abstractmethod
    def parse(self, file_path: str) -> list[T]:
        """
        Parse a file and return structured objects.
        """
        pass
