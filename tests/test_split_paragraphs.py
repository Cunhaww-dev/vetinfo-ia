from vetinfo_ia.adapters.text_file import group_sections, split_paragraphs


def test_split_paragraphs_splits_on_blank_line():
    text = "This is the first paragraph.\n\nThis is the second paragraph.\n\nThis is the third paragraph."
    expected_output = [
        "This is the first paragraph.",
        "This is the second paragraph.",
        "This is the third paragraph.",
    ]
    assert split_paragraphs(text) == expected_output


def test_split_paragraphs_removes_extra_newlines():
    text = "FÓRMULA:\n\n\nINDICAÇÕES:"
    result = split_paragraphs(text)
    assert result == ["FÓRMULA:", "INDICAÇÕES:"]


def test_group_sections_keeps_the_dose_table_with_its_title():
    paragraphs = [
        "POSOLOGIA:",
        "Para cães e gatos, a dose média recomendada é de:",
        "Até 2,5 kg: ½ comprimido",
        "CONTRA-INDICAÇÕES:",
        "Não administrar em filhotes com menos de 8 semanas.",
    ]

    sections = group_sections(paragraphs)

    assert sections == [
        "POSOLOGIA:\nPara cães e gatos, a dose média recomendada é de:\nAté 2,5 kg: ½ comprimido",
        "CONTRA-INDICAÇÕES:\nNão administrar em filhotes com menos de 8 semanas.",
    ]


def test_group_sections_keeps_text_before_the_first_title_as_one_section():
    paragraphs = ["USO VETERINÁRIO", "Coprovet®", "FÓRMULA:", "Tiamina 0,5 mg"]

    sections = group_sections(paragraphs)

    assert sections == ["USO VETERINÁRIO\nCoprovet®", "FÓRMULA:\nTiamina 0,5 mg"]


def test_group_sections_ignores_empty_paragraphs():
    assert group_sections(["FÓRMULA:", "", "Tiamina 0,5 mg"]) == [
        "FÓRMULA:\nTiamina 0,5 mg"
    ]
