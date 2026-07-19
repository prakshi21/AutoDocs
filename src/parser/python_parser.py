import ast
import logging
from models.code_symbol import CodeSymbol
from parser.base_parser import BaseParser
from parser.symbol_visitor import SymbolVisitor

logger = logging.getLogger(__name__)


class PythonParser(BaseParser[CodeSymbol]):

    @property
    def supported_extensions(self) -> set[str]:
        return {".py"}

    def parse(self, file_path: str) -> list[CodeSymbol]:

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)

            visitor = SymbolVisitor(file_path)

            visitor.visit(tree)

            return visitor.symbols

        except SyntaxError:
            logger.error(f"Syntax error in {file_path}")
            return []

        except Exception:
            logger.exception(f"Error parsing {file_path}")
            return []
