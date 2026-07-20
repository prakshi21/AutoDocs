from collections.abc import Iterator

from models.document_chunk import DocumentChunk


class DocumentChunkCollection:
    """
    Collection of DocumentChunks.
    """

    def __init__(self) -> None:
        self._chunks: list[DocumentChunk] = []

    def add(
        self,
        chunk: DocumentChunk,
    ) -> None:
        self._chunks.append(chunk)

    @property
    def count(self) -> int:
        return len(self._chunks)

    @property
    def chunks(self) -> list[DocumentChunk]:
        return self._chunks

    def __iter__(self) -> Iterator[DocumentChunk]:
        return iter(self._chunks)

    def __len__(self) -> int:
        return len(self._chunks)
