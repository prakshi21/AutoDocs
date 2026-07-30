from chunking.chunking_config import ChunkingConfig
from chunking.repository_chunker import RepositoryChunker
from chunking.semantic_splitter import SemanticSplitter
from chunking.token_counter import ApproximateTokenCounter
from embeddings.embeddings_config import EmbeddingConfig
from embeddings.embedding_generator import EmbeddingGenerator
from embeddings.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)
from llm.gemini_provider import GeminiProvider
from llm.llm_config import LLMConfig
from parser.markdown_parser import MarkdownParser
from parser.parser_registry import ParserRegistry
from parser.python_parser import PythonParser
from parser.repository_walker import RepositoryWalker
from pipeline.document_builder import RepositoryDocumentBuilder
from analyzer.repository_indexer import RepositoryIndexer
from qa.repository_qa import RepositoryQA
from retrieval.context_builder import ContextBuilder
from retrieval.query_embedder import QueryEmbedder
from retrieval.retriever import Retriever
from vector_store.chroma_config import ChromaConfig
from vector_store.chroma_vector_store import ChromaVectorStore


def build_repository_qa(
    repository_path: str,
) -> RepositoryQA:
    """
    Build the complete RepositoryQA pipeline.

    This function is responsible for:
        - Indexing the repository
        - Chunking
        - Embedding
        - Populating the vector store
        - Constructing the retrieval pipeline
    """

    # ---------------------------------------------------
    # Repository Indexing
    # ---------------------------------------------------

    walker = RepositoryWalker()
    registry = ParserRegistry()
    registry.register(PythonParser())
    registry.register(MarkdownParser())

    indexer = RepositoryIndexer(
        repository_walker=walker,
        parser_registry=registry,
    )

    repository_index = indexer.build(repository_path)

    # ---------------------------------------------------
    # Repository Documents
    # ---------------------------------------------------

    document_builder = RepositoryDocumentBuilder()

    documents = document_builder.build(repository_index)

    # ---------------------------------------------------
    # Chunking
    # ---------------------------------------------------

    chunker = RepositoryChunker(
        semantic_splitter=SemanticSplitter(),
        token_counter=ApproximateTokenCounter(),
        config=ChunkingConfig(),
    )

    chunks = chunker.chunk(documents)

    # ---------------------------------------------------
    # Embeddings
    # ---------------------------------------------------

    embedding_provider = SentenceTransformerEmbeddingProvider(EmbeddingConfig())

    embedding_generator = EmbeddingGenerator(embedding_provider)

    embeddings = embedding_generator.generate(chunks)

    # ---------------------------------------------------
    # Vector Store
    # ---------------------------------------------------

    vector_store = ChromaVectorStore(
        ChromaConfig(
            collection_name="repository",
        )
    )

    vector_store.add(embeddings)

    # ---------------------------------------------------
    # Retrieval Pipeline
    # ---------------------------------------------------

    query_embedder = QueryEmbedder(embedding_provider)

    retriever = Retriever(
        vector_store=vector_store,
        chunks=chunks,
    )

    context_builder = ContextBuilder()

    # ---------------------------------------------------
    # LLM
    # ---------------------------------------------------

    llm = GeminiProvider(
        LLMConfig(
            model_name="gemini-2.5-flash",
        )
    )

    # ---------------------------------------------------
    # QA
    # ---------------------------------------------------

    return RepositoryQA(
        query_embedder=query_embedder,
        retriever=retriever,
        context_builder=context_builder,
        llm=llm,
    )
