import ast

from models.entities import CodeSymbol
from models.enums import SymbolType


class SymbolVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.symbols: list[CodeSymbol] = []
        self.class_stack: list[str] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        class_name = node.name

        symbol = CodeSymbol(
            id=f"{self.file_path}::{class_name}",
            name=class_name,
            symbol_type=SymbolType.CLASS,
            file_path=self.file_path,
            start_line=node.lineno,
            end_line=node.end_lineno or node.lineno,
            signature=class_name,
            docstring=ast.get_docstring(node),
        )

        self.symbols.append(symbol)

        self.class_stack.append(class_name)

        self.generic_visit(node)

        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:

        if self.class_stack:
            class_name = self.class_stack[-1]
            symbol_type = SymbolType.METHOD
            display_name = f"{class_name}.{node.name}"
        else:
            symbol_type = SymbolType.FUNCTION
            display_name = node.name

        symbol = CodeSymbol(
            id=f"{self.file_path}::{display_name}",
            name=display_name,
            symbol_type=symbol_type,
            file_path=self.file_path,
            start_line=node.lineno,
            end_line=node.end_lineno or node.lineno,
            signature=self._build_signature(node),
            docstring=ast.get_docstring(node),
        )

        self.symbols.append(symbol)

        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def _build_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        args = [arg.arg for arg in node.args.args]

        return f"{node.name}({', '.join(args)})"
