from dataclasses import dataclass

from vetinfo_ia.domain.source import Source


class AnswerWithoutSourceError(Exception):
    """Raised when an answer is created without any source."""


@dataclass(frozen=True)
class Answer:
    text: str
    # tupla e não lista: com lista daria pra fazer answer.sources.append(...)
    # e alterar a resposta por dentro
    sources: tuple[Source, ...]

    def __post_init__(self) -> None:
        if not self.sources:
            raise AnswerWithoutSourceError("An answer must have at least one source.")
