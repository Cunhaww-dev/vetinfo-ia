from vetinfo_ia import split_paragraphs


def test_split_paragraphs():
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
