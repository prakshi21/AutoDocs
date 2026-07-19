from parser.markdown_parser import MarkdownParser
from parser.parser_registry import ParserRegistry
from parser.python_parser import PythonParser


def test_register_parsers():
    registry = ParserRegistry()

    registry.register(PythonParser())
    registry.register(MarkdownParser())

    assert ".py" in registry.supported_extensions
    assert ".md" in registry.supported_extensions


def test_get_python_parser():
    registry = ParserRegistry()

    registry.register(PythonParser())

    parser = registry.get_parser("auth.py")

    assert isinstance(parser, PythonParser)


def test_get_markdown_parser():
    registry = ParserRegistry()

    registry.register(MarkdownParser())

    parser = registry.get_parser("README.md")

    assert isinstance(parser, MarkdownParser)


def test_unknown_extension():
    registry = ParserRegistry()

    registry.register(PythonParser())

    assert registry.get_parser("image.png") is None


def test_duplicate_registration():
    import pytest

    registry = ParserRegistry()

    registry.register(PythonParser())

    with pytest.raises(ValueError):
        registry.register(PythonParser())
