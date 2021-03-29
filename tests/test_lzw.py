import pytest

from scicomp.exam.kk.lzw import lzw_decode, lzw_encode
from utils import _alphabet, random_strings


@pytest.mark.parametrize('seq', random_strings(10, 1000, 100))
def test_lzw(seq):
    assert all(a == b for a, b in zip(lzw_decode(lzw_encode(seq, _alphabet), _alphabet), seq))
