import sys

from vetinfo_ia.adapters.excerpt_model import ExcerptModel
from vetinfo_ia.adapters.keyword_search import KeywordSearch
from vetinfo_ia.adapters.text_file import load_chunks
from vetinfo_ia.application.answer_question import AnswerQuestion

BULA_PATH = "dados/coprovet.txt"


def main() -> None:
    if len(sys.argv) < 2:
        print('Uso: uv run vetinfo-ia "sua pergunta"')
        return

    question = sys.argv[1]

    try:
        chunks = load_chunks(BULA_PATH)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {BULA_PATH}")
        return

    use_case = AnswerQuestion(search=KeywordSearch(chunks), model=ExcerptModel())
    answer = use_case.execute(question)

    if answer is None:
        print("Não encontrei essa informação nas bulas.")
        return

    print(answer.text)
    print()
    print("Fontes:")
    for source in answer.sources:
        print(f"- {source.document}, página {source.page}")
