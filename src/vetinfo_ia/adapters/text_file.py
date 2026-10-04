from pathlib import Path

from vetinfo_ia.domain.chunk import Chunk


def read_bula(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        bula = f.read()
    return bula


def split_paragraphs(text: str) -> list[str]:
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs]


def is_section_title(paragraph: str) -> bool:
    """Título de seção de bula: tudo em maiúsculas e terminando em dois-pontos."""
    return paragraph.isupper() and paragraph.endswith(":")


def group_sections(paragraphs: list[str]) -> list[str]:
    """Junta cada título de seção com os parágrafos que vêm depois dele.

    Assim a tabela de dose fica no mesmo trecho que o título POSOLOGIA,
    em vez de virar um pedaço solto sem contexto.
    """
    sections: list[list[str]] = []
    for paragraph in paragraphs:
        if not paragraph:
            continue
        if is_section_title(paragraph) or not sections:
            sections.append([paragraph])
        else:
            sections[-1].append(paragraph)
    return ["\n".join(section) for section in sections]


def load_chunks(file_path: str) -> list[Chunk]:
    """Lê uma bula em .txt e devolve um Chunk por seção.

    Arquivo .txt não tem página, então todo trecho sai como página 1.
    """
    text = read_bula(file_path)
    sections = group_sections(split_paragraphs(text))
    document = Path(file_path).name
    return [Chunk(text=section, document=document, page=1) for section in sections]
