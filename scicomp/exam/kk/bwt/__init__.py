import bisect
from typing import Iterable, Sequence, TypeVar

from more_itertools import bucket

from .collections import OrderedListDict
from .end_marker import _end_marker
from .suffix_array import suffix_array


__all__ = 'bwt_encode', 'bwt_decode'


_T = TypeVar('_T')


def bwt_encode(seq: Iterable[_T]) -> Iterable[_T]:
    """
    Burrows-Wheeler transform (forward).

    Args:
        seq: the sequence to encode

    Returns:
        The Burrows-Wheeler encoded `seq`.

    See Also:
        `bwt_decode`
    """
    if isinstance(seq, str):
        seq = list(seq)
        if seq[-1] == '\0':
            seq[-1] = _end_marker
    if not isinstance(seq, Sequence):
        seq = list(seq)
    return (seq[i-1] if i != 0 else _end_marker for i in suffix_array(seq))


def bwt_decode(seq: Iterable[_T]) -> Iterable[_T]:
    """
    Burrows-Wheeler transform (reverse).

    Args:
        seq: the string to decode

    Returns:
        The Burrows-Wheeler decoded `s`.

    See Also:
        `bwt_encode`
    """
    if not isinstance(seq, Sequence):
        seq = list(seq)

    # Build two data structures:
    #   - mpng: maps an element to an array of indices at which it occurs
    #           lookups in mpng are O(size of alphabet)
    #   - bucks: boundaries of buckets by element; again O(f(|alphabet|))
    mpng, bucks = (f(a) for f, a in zip((OrderedListDict, lambda x: x), zip(*(
        ((key, lbk), total)
        for total in [0]
        for key, lbk in sorted(
            (key, list(b[key])) for b in [
                bucket(range(len(seq)), lambda i: seq[i])
            ] for key in b)
        for total in [total + len(lbk)]))))

    # Each next element is the label of the bucket of the i-th occurence of
    # the current element, where i is the position in the cureent bucket of
    # the current position.
    return (el for i in [seq.index(_end_marker)] for _ in range(len(seq) - 1)
            for li in [bisect.bisect_left(bucks, i + 1)]
            for el in [mpng.data[li][0]]
            for i in [mpng[el][i - bucks[li - 1]]])
