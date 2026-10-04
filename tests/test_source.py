from dataclasses import FrozenInstanceError

import pytest

from vetinfo_ia.domain.source import Source


def test_sources_with_same_data_are_equal():
    a = Source(document="coprovet.pdf", page=1, excerpt="Administrar por via oral.")
    b = Source(document="coprovet.pdf", page=1, excerpt="Administrar por via oral.")

    assert a == b


def test_source_cannot_be_changed():
    source = Source(
        document="coprovet.pdf", page=1, excerpt="Administrar por via oral."
    )

    with pytest.raises(FrozenInstanceError):
        source.excerpt = "Administrar por via intravenosa."
