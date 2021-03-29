import bisect
from typing import Iterable, Sequence, TypeVar

from more_itertools import bucket

from .collections import OrderedListDict
from .end_marker import _end_marker
from .suffix_array import suffix_array


__all__ = 'bwt_encode', 'bwt_decode'


_T = TypeVar('_T')


def bwt_encode(seq: Iterable[_T]) -> Iterable[_T]:
    r"""Burrows-Wheeler transform (forward) using suffix arrays.

    Args:
        seq: the sequence to encode. If not a `collections.abc.Sequence`, it
            will be implicitly converted to a `list`. Also, an end marker is
            not strictly required and will be appended automatically. If `seq`
            is a string, a zero byte (``'\0'``) is recognised as an end marker
            and converted to the internal representation.

    Returns:

        The Burrows-Wheeler encoded `seq`. See
        `Wikipedia <https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform>`_
        for more details.

    Warnings:
        Returns an iterator, so make sure to "consume" it before e.g. saving,
        or if you plan to re-use the result.

    See Also:
        `bwt_decode`
    """
    if isinstance(seq, str):
        seq = list(seq)
        if seq[-1] == '\0':
            seq[-1] = _end_marker
    return (seq[i-1] if i != 0 else _end_marker for i in suffix_array(seq))


def bwt_decode(seq: Iterable[_T]) -> Iterable[_T]:
    """Burrows-Wheeler transform (reverse).

    Method due to Gusfield `[link] <https://www.cs.ucdavis.edu/~gusfield/cs224f11/BWTcs224.pdf>`_.

    Args:
        seq: the sequence to decode. In practice any iterables are accepted,
            particularly the result of `bwt_encode`. Note that the end marker
            **has** to be the internal representation. The easiest way to get
            it right is to use `bwt_encode`, and you should build custom
            sequences to decode only if you know what you're doing.

    Returns:

        The Burrows-Wheeler decoded `seq`. It is generally not of the same
        object type as the original, though, so care should be taken to do
        item-by-item comparison, especially with strings, which get decoded
        into an iterator of length-one strings (characters).

    Warnings:
        Returns an iterator, so make sure to "consume" it before e.g. saving,
        or if you plan to re-use the result.

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
