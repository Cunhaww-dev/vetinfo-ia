from vetinfo_ia.application.ports import AnswerModel, ChunkSearch
from vetinfo_ia.domain.answer import Answer
from vetinfo_ia.domain.source import Source


class AnswerQuestion:
    def __init__(self, search: ChunkSearch, model: AnswerModel) -> None:
        self._search = search
        self._model = model

    def execute(self, question: str) -> Answer | None:
        chunks = self._search.search(question)
        if not chunks:
            return None
        text = self._model.generate(question, chunks)
        sources = tuple(
            Source(document=c.document, page=c.page, excerpt=c.text) for c in chunks
        )
        return Answer(text=text, sources=sources)
