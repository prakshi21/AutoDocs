from models.document_type import DocumentType
from models.repository_document import RepositoryDocument


class SemanticSplitter:
    """
    Splits RepositoryDocuments into semantically meaningful text pieces.
    """

    def split(
        self,
        document: RepositoryDocument,
    ) -> list[str]:
        """
        Split a repository document into semantic pieces.
        """

        if document.document_type == DocumentType.DOCUMENTATION:
            return self._split_documentation(document)

        return self._split_symbol(document)

    @staticmethod
    def _is_code_fence(line: str) -> bool:
        """
        Return True if the line starts or ends a fenced code block.
        """
        return line.strip().startswith("```")

    @staticmethod
    def _is_heading(line: str) -> bool:
        """
        Return True if the line is a Markdown heading.
        """
        stripped = line.lstrip()

        return (
            stripped.startswith("# ")
            or stripped.startswith("## ")
            or stripped.startswith("### ")
            or stripped.startswith("#### ")
            or stripped.startswith("##### ")
            or stripped.startswith("###### ")
        )

    def _flush_current(
        self,
        pieces: list[str],
        current: list[str],
    ) -> list[str]:
        """
        Flush the current semantic piece into the output.
        """

        if current:
            pieces.append("\n".join(current).strip())

        return []

    def _split_documentation(
        self,
        document: RepositoryDocument,
    ) -> list[str]:
        """
        Split documentation into semantic paragraphs while preserving
        fenced code blocks.
        """

        pieces: list[str] = []
        current: list[str] = []

        inside_code_block = False

        for line in document.content.splitlines():

            stripped = line.strip()

            if self._is_code_fence(line):
                inside_code_block = not inside_code_block
                current.append(line)
                continue

            if inside_code_block:
                current.append(line)
                continue

            if not inside_code_block and self._is_heading(line):
                current = self._flush_current(
                    pieces,
                    current,
                )

                current.append(line)

                continue

            if stripped:
                current.append(line)
            else:
                current = self._flush_current(
                    pieces,
                    current,
                )

        self._flush_current(
            pieces,
            current,
        )

        return pieces

    def _split_symbol(
        self,
        document: RepositoryDocument,
    ) -> list[str]:
        """
        Keep symbols intact.

        Code symbols already represent one semantic unit.
        """

        return [document.content]
