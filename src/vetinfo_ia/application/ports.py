from typing import Protocol

from vetinfo_ia.domain.chunk import Chunk


class ChunkSearch(Protocol):
    def search(self, question: str) -> list[Chunk]: ...


class AnswerModel(Protocol):
    def generate(self, question: str, chunks: list[Chunk]) -> str: ...
