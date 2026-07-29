from collections.abc import Iterator

from models.document_chunk import DocumentChunk


class DocumentChunkCollection:
    """
    Collection of DocumentChunks.
    """

    def __init__(self) -> None:
        self._chunks: list[DocumentChunk] = []
        self._chunk_index: dict[str, DocumentChunk] = {}

    def add(
        self,
        chunk: DocumentChunk,
    ) -> None:
        self._chunks.append(chunk)
        self._chunk_index[chunk.id] = chunk

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

    def get_by_id(
        self,
        chunk_id: str,
    ) -> DocumentChunk | None:
        """
        Return a chunk by its ID.
        """
        return self._chunk_index.get(chunk_id)
