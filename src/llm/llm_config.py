from dataclasses import dataclass


@dataclass(slots=True)
class LLMConfig:
    """
    Configuration for LLM providers.
    """

    model_name: str

    temperature: float = 0.2

    max_output_tokens: int = 1024
