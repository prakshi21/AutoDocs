from pathlib import Path

from parser.base_parser import BaseParser


class ParserRegistry:
    """
    Registry responsible for resolving the correct parser
    for a given file extension.
    """

    def __init__(self) -> None:
        self._parsers: dict[str, BaseParser] = {}

    def register(self, parser: BaseParser) -> None:
        """
        Register a parser for all supported extensions.
        """

        for extension in parser.supported_extensions:

            if extension in self._parsers:
                raise ValueError(f"Parser already registered for '{extension}'")

            self._parsers[extension] = parser

    def get_parser(self, file_path: str) -> BaseParser | None:
        """
        Return the parser responsible for a file.
        """

        extension = Path(file_path).suffix.lower()

        return self._parsers.get(extension)

    def supports(self, file_path: str) -> bool:
        """
        Check whether a parser exists for a file.
        """

        return self.get_parser(file_path) is not None

    @property
    def supported_extensions(self) -> set[str]:
        return set(self._parsers.keys())
