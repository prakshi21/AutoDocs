from analyzer.repository_indexer import RepositoryIndexer
from parser.markdown_parser import MarkdownParser
from parser.parser_registry import ParserRegistry
from parser.python_parser import PythonParser
from parser.repository_walker import RepositoryWalker
from pipeline.document_builder import RepositoryDocumentBuilder


def main() -> None:
    registry = ParserRegistry()
    registry.register(PythonParser())
    registry.register(MarkdownParser())

    walker = RepositoryWalker()

    indexer = RepositoryIndexer(
        repository_walker=walker,
        parser_registry=registry,
    )

    repository_index = indexer.build("sample_repo")

    builder = RepositoryDocumentBuilder()

    collection = builder.build(repository_index)

    print("=" * 80)

    for document in collection:
        print(f"Title : {document.title}")
        print(f"Type  : {document.document_type.value}")
        print(f"ID    : {document.id}")
        print("Metadata")
        print(document.metadata)
        print("-" * 80)
        print(document.content)
        print("=" * 80)


if __name__ == "__main__":
    main()
