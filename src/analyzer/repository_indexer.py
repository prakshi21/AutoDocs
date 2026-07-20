from .repository_index import RepositoryIndex

from models.artifact import ParsedArtifact
from models.code_symbol import CodeSymbol
from models.document_section import DocumentSection

from parser.parser_registry import ParserRegistry
from parser.repository_walker import RepositoryWalker


class RepositoryIndexer:
    """
    Orchestrates the repository indexing pipeline.

    Responsibilities:
    - Walk the repository
    - Select the appropriate parser for each file
    - Parse supported files
    - Build a RepositoryIndex
    """

    def __init__(
        self,
        repository_walker: RepositoryWalker,
        parser_registry: ParserRegistry,
    ) -> None:
        self._walker = repository_walker
        self._registry = parser_registry

    def build(self, repository_path: str) -> RepositoryIndex:
        """
        Build a RepositoryIndex for an entire repository.

        Args:
            repository_path: Path to the repository root.

        Returns:
            A populated RepositoryIndex.
        """

        index = RepositoryIndex()

        files = self._walker.walk(repository_path)

        for file_path in files:

            parser = self._registry.get_parser(file_path)

            if parser is None:
                continue

            artifacts = parser.parse(file_path)

            for artifact in artifacts:
                self._add_artifact(index, artifact)

        return index

    def _add_artifact(
        self,
        index: RepositoryIndex,
        artifact: ParsedArtifact,
    ) -> None:
        """
        Add a parsed artifact to the repository index.

        Args:
            index: Repository index being constructed.
            artifact: Parsed artifact returned by a parser.

        Raises:
            TypeError: If the artifact type is unsupported.
        """

        if isinstance(artifact, CodeSymbol):
            index.add_symbol(artifact)
            return

        if isinstance(artifact, DocumentSection):
            index.add_document(artifact)
            return

        raise TypeError(f"Unsupported artifact type: {type(artifact).__name__}")
