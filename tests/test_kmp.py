from random import randint, random

import pytest

from scicomp.exam.kk import kmp_search
from utils import _get_random_string, random_strings


@pytest.mark.parametrize(
    ('seq', 'subseq_size'), (
        (s, randint(0, len(s)) if random() > 0.42 else -1)
        for s in random_strings(100, 1000, N=10000)
    )
)
def test_kmp(seq: str, subseq_size: int):
    subseq = _get_random_string(randint(0, len(seq))) if subseq_size < 0 else seq[randint(0, len(seq)-subseq_size):][:subseq_size]
    assert kmp_search(subseq, seq) == (None if ((truth := seq.find(subseq)) == -1) else truth)
