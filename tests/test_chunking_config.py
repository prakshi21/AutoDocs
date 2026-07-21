from chunking.chunking_config import ChunkingConfig


def test_default_values():
    config = ChunkingConfig()

    assert config.max_tokens == 512
    assert config.chunk_overlap == 0
    assert config.preserve_headings is True
    assert config.preserve_code_blocks is True
    assert config.min_chunk_size == 0


def test_custom_values():
    config = ChunkingConfig(
        max_tokens=256,
        chunk_overlap=32,
        preserve_headings=False,
        preserve_code_blocks=False,
        min_chunk_size=20,
    )

    assert config.max_tokens == 256
    assert config.chunk_overlap == 32
    assert config.preserve_headings is False
    assert config.preserve_code_blocks is False
    assert config.min_chunk_size == 20
