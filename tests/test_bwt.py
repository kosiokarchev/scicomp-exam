from itertools import zip_longest

import pytest
from more_itertools import circular_shifts, last

from scicomp.exam.kk.bwt import _end_marker, bwt_decode, bwt_encode
from utils import random_strings



@pytest.mark.parametrize(
    's', (s for s in random_strings(100, 5000, N=100)))
def test_bwt_encode(s):
    assert all(
        a == (b if b != '\0' else _end_marker)
        for a, b in zip_longest(
            bwt_encode(s),
            map(last, sorted(circular_shifts(s + '\0')))  # <- python rulzz!!
        )
    )


@pytest.mark.parametrize(
    's', (s for s in random_strings(100, 5000, N=100)))
def test_bwt_roundtrip(s):
    assert ''.join(bwt_decode(bwt_encode(s))) == s
