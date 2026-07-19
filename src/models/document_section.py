from dataclasses import dataclass


@dataclass
class DocumentSection:
    id: str
    title: str
    content: str
    file_path: str
    level: int
    start_line: int
    end_line: int


# Alias Documentation to DocumentSection
Documentation = DocumentSection
