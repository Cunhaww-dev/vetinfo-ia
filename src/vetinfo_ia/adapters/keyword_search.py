import re
import unicodedata

from vetinfo_ia.domain.chunk import Chunk

# Palavras que aparecem em quase toda pergunta e não ajudam a achar o trecho.
STOPWORDS = {
    "qual",
    "quais",
    "como",
    "para",
    "com",
    "que",
    "uma",
    "dos",
    "das",
    "por",
    "pode",
    "deve",
    "esse",
    "essa",
    "este",
    "esta",
}


def normalize(text: str) -> str:
    """Minúsculas e sem acento, pra "POSOLOGIA" casar com "posologia"."""
    without_accents = unicodedata.normalize("NFD", text)
    return "".join(
        c for c in without_accents if unicodedata.category(c) != "Mn"
    ).lower()


def keywords(text: str) -> set[str]:
    words = re.findall(r"\w+", normalize(text))
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


class KeywordSearch:
    """Adaptador simples da porta ChunkSearch: busca por palavras em comum.

    Não entende significado: "filhote" não acha "menos de 8 semanas".
    Serve pra rodar o sistema de ponta a ponta antes de existir o pgvector,
    que entra na Fase 4 como outro adaptador da mesma porta.
    """

    def __init__(self, chunks: list[Chunk], limit: int = 2) -> None:
        self._chunks = chunks
        self._limit = limit

    def search(self, question: str) -> list[Chunk]:
        question_words = keywords(question)
        scored = [(self._score(question_words, chunk), chunk) for chunk in self._chunks]
        matches = [(score, chunk) for score, chunk in scored if score > 0]
        matches.sort(key=lambda pair: pair[0], reverse=True)
        return [chunk for _, chunk in matches[: self._limit]]

    def _score(self, question_words: set[str], chunk: Chunk) -> int:
        """Uma palavra em comum vale 1 ponto, e vale 2 se estiver no título do trecho.

        Sem isso, "qual a posologia?" empata entre a seção POSOLOGIA e qualquer
        outra que só cite a palavra no meio do texto.
        """
        title = chunk.text.split("\n")[0]
        in_text = len(question_words & keywords(chunk.text))
        in_title = len(question_words & keywords(title))
        return in_text + in_title
