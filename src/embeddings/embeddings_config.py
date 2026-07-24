# src/embeddings/embedding_config.py

from dataclasses import dataclass


@dataclass(slots=True)
class EmbeddingConfig:
    model_name: str = "all-MiniLM-L6-v2"
