from analyzer.repository_indexer import RepositoryIndexer
from parser.markdown_parser import MarkdownParser
from parser.parser_registry import ParserRegistry
from parser.python_parser import PythonParser
from parser.repository_walker import RepositoryWalker


def main() -> None:
    registry = ParserRegistry()
    registry.register(PythonParser())
    registry.register(MarkdownParser())

    walker = RepositoryWalker()

    indexer = RepositoryIndexer(
        repository_walker=walker,
        parser_registry=registry,
    )

    index = indexer.build("sample_repo")

    print("=" * 60)
    print("Repository Summary")
    print("=" * 60)

    print(f"Symbols: {index.symbol_count}")
    print(f"Documents: {index.document_count}")

    print("\nCode Symbols")
    print("-" * 60)

    for symbol in index.all_symbols:
        print(
            f"{symbol.symbol_type.value:10}" f"{symbol.name:25}" f"{symbol.file_path}"
        )

    print("\nMarkdown Sections")
    print("-" * 60)

    for section in index.all_documents:
        print(f"L{section.level} " f"{section.title}")


if __name__ == "__main__":
    main()
