from analyzer.repository_indexer import RepositoryIndexer
from chunking.chunking_config import ChunkingConfig
from chunking.repository_chunker import RepositoryChunker
from chunking.semantic_splitter import SemanticSplitter
from chunking.token_counter import ApproximateTokenCounter
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

    config = ChunkingConfig()

    chunker = RepositoryChunker(
        semantic_splitter=SemanticSplitter(),
        token_counter=ApproximateTokenCounter(),
        config=config,
    )

    chunks = chunker.chunk(collection)

    print("=" * 80)

    for chunk in chunks:
        print(f"ID     : {chunk.id}")
        print(f"Parent : {chunk.parent_document_id}")
        print(f"Index  : {chunk.chunk_index}")
        print("Metadata")
        print(chunk.metadata)
        print("-" * 80)
        print(chunk.content)
        print("=" * 80)


if __name__ == "__main__":
    main()

