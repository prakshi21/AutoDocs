import logging
import re

from models.document_section import DocumentSection
from parser.base_parser import BaseParser

logger = logging.getLogger(__name__)


class MarkdownParser(BaseParser[DocumentSection]):
    HEADING_REGEX = re.compile(r"^(#{1,6})\s+(.*)$")

    @property
    def supported_extensions(self) -> set[str]:
        return {
            ".md",
            ".markdown",
        }

    def parse(self, file_path: str) -> list[DocumentSection]:
        sections: list[DocumentSection] = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

        except FileNotFoundError:
            logger.error("Markdown file not found: %s", file_path)
            return []

        except Exception:
            logger.exception("Failed to read markdown file: %s", file_path)
            return []

        if not lines:
            return []

        current_title = "ROOT"
        current_level = 0
        current_start_line = 1
        current_content: list[str] = []

        for line_number, line in enumerate(lines, start=1):

            match = self.HEADING_REGEX.match(line.rstrip())

            if match:

                # Save previous section
                if current_content or current_title == "ROOT":
                    sections.append(
                        self._create_section(
                            file_path=file_path,
                            title=current_title,
                            level=current_level,
                            start_line=current_start_line,
                            end_line=line_number - 1,
                            content=current_content,
                        )
                    )

                current_level = len(match.group(1))
                current_title = match.group(2).strip()
                current_start_line = line_number

                # Do NOT include heading text in the content
                current_content = []

            else:
                current_content.append(line)

        # Save last section
        sections.append(
            self._create_section(
                file_path=file_path,
                title=current_title,
                level=current_level,
                start_line=current_start_line,
                end_line=len(lines),
                content=current_content,
            )
        )

        return sections

    def _create_section(
        self,
        file_path: str,
        title: str,
        level: int,
        start_line: int,
        end_line: int,
        content: list[str],
    ) -> DocumentSection:

        text = "".join(content).strip()

        return DocumentSection(
            id=f"{file_path}::{title}",
            title=title,
            content=text,
            file_path=file_path,
            level=level,
            start_line=start_line,
            end_line=end_line,
        )
