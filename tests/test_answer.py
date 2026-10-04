import pytest

from vetinfo_ia.domain.answer import Answer, AnswerWithoutSourceError
from vetinfo_ia.domain.source import Source


def test_answer_keeps_text_and_sources():
    source = Source(
        document="coprovet.pdf", page=1, excerpt="Administrar por via oral."
    )

    answer = Answer(text="O Coprovet é administrado por via oral.", sources=(source,))

    assert answer.text == "O Coprovet é administrado por via oral."
    assert answer.sources == (source,)


def test_answer_keeps_every_source_in_order():
    dosage = Source(
        document="coprovet.pdf", page=1, excerpt="Até 2,5 kg: ½ comprimido."
    )
    warning = Source(
        document="coprovet.pdf",
        page=2,
        excerpt="Não administrar em filhotes com menos de 8 semanas.",
    )

    answer = Answer(
        text="Meio comprimido até 2,5 kg, exceto em filhotes com menos de 8 semanas.",
        sources=(dosage, warning),
    )

    assert answer.sources == (dosage, warning)


def test_answer_without_source_cannot_be_created():
    with pytest.raises(AnswerWithoutSourceError):
        Answer(text="A dose é de 2 comprimidos.", sources=())
