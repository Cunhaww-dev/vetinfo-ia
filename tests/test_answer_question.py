from vetinfo_ia.application.answer_question import AnswerQuestion
from vetinfo_ia.domain.chunk import Chunk
from vetinfo_ia.domain.source import Source


class FakeSearch:
    """Adaptador falso da porta ChunkSearch: devolve sempre os mesmos trechos."""

    def __init__(self, chunks: list[Chunk]) -> None:
        self._chunks = chunks

    def search(self, question: str) -> list[Chunk]:
        return self._chunks


class FakeModel:
    """Adaptador falso da porta AnswerModel: responde sempre a mesma frase."""

    def __init__(self) -> None:
        self.was_called = False

    def generate(self, question: str, chunks: list[Chunk]) -> str:
        self.was_called = True
        return "Administrar por via oral."


DOSAGE = Chunk(text="Até 2,5 kg: ½ comprimido.", document="coprovet.pdf", page=1)
ROUTE = Chunk(text="Administrar por via oral.", document="coprovet.pdf", page=2)


def test_answers_with_the_model_text_and_cites_every_chunk_found():
    use_case = AnswerQuestion(search=FakeSearch([DOSAGE, ROUTE]), model=FakeModel())

    answer = use_case.execute("Como administrar o Coprovet?")

    assert answer is not None
    assert answer.text == "Administrar por via oral."
    assert answer.sources == (
        Source(document="coprovet.pdf", page=1, excerpt="Até 2,5 kg: ½ comprimido."),
        Source(document="coprovet.pdf", page=2, excerpt="Administrar por via oral."),
    )


def test_returns_nothing_when_no_chunk_is_found():
    use_case = AnswerQuestion(search=FakeSearch([]), model=FakeModel())

    answer = use_case.execute("Qual a dose de dipirona para cavalos?")

    assert answer is None


def test_does_not_call_the_model_when_no_chunk_is_found():
    model = FakeModel()
    use_case = AnswerQuestion(search=FakeSearch([]), model=model)

    use_case.execute("Qual a dose de dipirona para cavalos?")

    assert model.was_called is False
