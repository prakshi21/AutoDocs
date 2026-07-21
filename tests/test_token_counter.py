from typing import assert_type

from chunking.token_counter import (
    ApproximateTokenCounter,
    TokenCounter,
)


def test_protocol():
    counter: TokenCounter = ApproximateTokenCounter()

    assert_type(counter, TokenCounter)


def test_empty_string():
    counter = ApproximateTokenCounter()

    assert counter.count("") == 0


def test_single_word():
    counter = ApproximateTokenCounter()

    assert counter.count("hello") == 1


def test_multiple_words():
    counter = ApproximateTokenCounter()

    assert counter.count("hello world from autodocs") == 4


def test_multiple_spaces():
    counter = ApproximateTokenCounter()

    assert counter.count("hello     world") == 2


def test_newlines():
    counter = ApproximateTokenCounter()

    assert counter.count("hello\nworld\nagain") == 3


def test_tabs():
    counter = ApproximateTokenCounter()

    assert counter.count("hello\tworld") == 2
