from dataclasses import dataclass


@dataclass(slots=True)
class ChromaConfig:
    """
    Configuration for the Chroma vector store.
    """

    persist_directory: str = "./chroma_db"

    collection_name: str = "repository"

    distance_function: str = "cosine"
