from vetinfo_ia.domain.chunk import Chunk


class ExcerptModel:
    """Adaptador sem IA da porta AnswerModel: devolve o trecho mais relevante.

    Não escreve resposta nenhuma, só repete o que está na bula.
    Na Fase 5 o Claude entra como outro adaptador da mesma porta.
    """

    def generate(self, question: str, chunks: list[Chunk]) -> str:
        return chunks[0].text
