from dataclasses import dataclass
from typing import Optional
from models.enums import SymbolType


@dataclass
class CodeSymbol:
    id: str
    name: str
    symbol_type: SymbolType
    file_path: str
    parent: Optional[str] = None
    start_line: int = 0
    end_line: int = 0
    signature: str = ""
    docstring: Optional[str] = None


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
