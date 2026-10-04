from vetinfo_ia.adapters.excerpt_model import ExcerptModel
from vetinfo_ia.adapters.keyword_search import KeywordSearch
from vetinfo_ia.adapters.text_file import load_chunks
from vetinfo_ia.application.answer_question import AnswerQuestion
from vetinfo_ia.domain.chunk import Chunk

DOSAGE = Chunk(
    text="POSOLOGIA:\nAté 2,5 kg: ½ comprimido", document="coprovet.txt", page=1
)
WARNING = Chunk(
    text="CONTRA-INDICAÇÕES:\nNão administrar em filhotes com menos de 8 semanas.",
    document="coprovet.txt",
    page=1,
)


def test_finds_the_chunk_that_shares_words_with_the_question():
    search = KeywordSearch([DOSAGE, WARNING])

    assert search.search("Posso dar para filhotes?") == [WARNING]


def test_ignores_accents_and_capital_letters():
    search = KeywordSearch([DOSAGE, WARNING])

    assert search.search("qual a posologia?") == [DOSAGE]


def test_returns_nothing_when_no_word_matches():
    search = KeywordSearch([DOSAGE, WARNING])

    assert search.search("Qual a dose de dipirona para cavalos?") == []


def test_returns_the_best_match_first_and_respects_the_limit():
    search = KeywordSearch([DOSAGE, WARNING], limit=1)

    result = search.search("administrar em filhotes com 8 semanas e 2 kg")

    assert result == [WARNING]


def test_whole_flow_with_the_real_bula():
    """Ponta a ponta com o arquivo real: pergunta, busca, resposta e fonte."""
    chunks = load_chunks("dados/coprovet.txt")
    use_case = AnswerQuestion(search=KeywordSearch(chunks), model=ExcerptModel())

    answer = use_case.execute("Qual a posologia?")

    assert answer is not None
    assert "Até 2,5 kg" in answer.text
    assert answer.sources[0].document == "coprovet.txt"


def test_whole_flow_says_nothing_for_a_question_outside_the_bula():
    chunks = load_chunks("dados/coprovet.txt")
    use_case = AnswerQuestion(search=KeywordSearch(chunks), model=ExcerptModel())

    assert use_case.execute("Qual o preço do Bravecto?") is None
