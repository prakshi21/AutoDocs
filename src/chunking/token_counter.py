from typing import Protocol
import re


class TokenCounter(Protocol):
    """
    Interface for estimating or counting tokens in text.

    Different implementations may use approximate heuristics
    or model-specific tokenizers.
    """

    def count(
        self,
        text: str,
    ) -> int:
        """
        Return the number of tokens in the given text.
        """
        ...


class ApproximateTokenCounter:
    """
    Approximate token counter based on whitespace-separated words.

    This implementation is lightweight and fast. It can later be
    replaced with a model-specific tokenizer without affecting
    the rest of the chunking pipeline.
    """

    WORD_PATTERN = re.compile(r"\S+")

    def count(
        self,
        text: str,
    ) -> int:
        """
        Estimate the number of tokens in the text.
        """
        return len(self.WORD_PATTERN.findall(text))
