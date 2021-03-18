import pytest
from more_itertools import collapse

from scicomp.exam.kk.lzw import lzw_decode, lzw_encode
from utils import _alphabet, random_strings


@pytest.mark.parametrize('seq', random_strings(10, 1000, 100))
def test_lzw(seq):
    assert tuple(collapse(lzw_decode(lzw_encode(seq, _alphabet), _alphabet))) == tuple(seq)
