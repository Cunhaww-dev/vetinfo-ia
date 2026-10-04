from dataclasses import FrozenInstanceError

import pytest

from vetinfo_ia.domain.chunk import Chunk


def test_chunks_with_same_data_are_equal():
    a = Chunk(text="Administrar por via oral.", document="coprovet.pdf", page=1)
    b = Chunk(text="Administrar por via oral.", document="coprovet.pdf", page=1)

    assert a == b


def test_chunk_cannot_be_changed():
    chunk = Chunk(text="Administrar por via oral.", document="coprovet.pdf", page=1)

    with pytest.raises(FrozenInstanceError):
        chunk.text = "Administrar por via intravenosa."
