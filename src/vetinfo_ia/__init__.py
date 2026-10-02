# no nível do arquivo só ficam definições (def, class, constantes); ação fica dentro de função.


def read_bula(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        bula = f.read()
    return bula


def split_paragraphs(text: str) -> list[str]:
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs]


def main() -> None:
    file_path = "dados/coprovet.txt"
    try:
        bula = read_bula(file_path)
    except FileNotFoundError:
        print(f"File not found, please check, {file_path}")
        return

    bula_paragraphs = split_paragraphs(bula)
    first_paragraph = bula_paragraphs[0]
    paragraph_count = len(bula_paragraphs)
    longest_paragraph = max(bula_paragraphs, key=len)
    total_characters = len(longest_paragraph)

    print(f"First paragraph: {first_paragraph}")
    print(f"Quantity of paragraphs: {paragraph_count}")
    print(f"Longest paragraph: {longest_paragraph}")
    print(f"Total characters in Longest paragraph: {total_characters}")
