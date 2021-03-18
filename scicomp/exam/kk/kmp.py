from itertools import islice
from typing import Iterable, Optional, Sequence, TypeVar

from more_itertools import first


_T = TypeVar('_T')


def _kmp_table(seq: Sequence[_T]) -> Sequence[int]:
    """Compute the KMP partial match "table"."""
    return [
        j
        for j in [-1]
        for cur in seq
        for j in [j+1 if cur == seq[j] else 0]
    ]


def kmp_search(needle: Sequence[_T], haystack: Iterable[_T]) -> Optional[int]:
    """
    Find the first occurence of `seq` in `haystack`.

    Args:
        needle: subsequence to search form
        haystack: sequence to search in

    Returns:
        The index of the first occurence of `seq` in `haystack` or `None` if
            not found. In general,::

                haystack[kmp_search(needle, haystack):][:len(needle)] == needle

            which means that, like the builtin `index`/`find` methods, for an
            empty `needle`, this returns ``0``.
    """
    t = _kmp_table(needle)
    return next((
        i-j+1
        for j in [0]  # initialise
        for i, cur in enumerate(haystack)  # indeed, cycle only once through haystack!:
        # next line is for debug:
        # for _ in [print(cur, needle[j], j)]
        # checks here allow the table building to be slightly simpler
        # and to allow a non-sequence iterable haystack
        for j in [(j if needle[j] == cur else t[j-1] if j > 0 else -1) + 1]
        # if starting all over, check current against the first:
        for j in [j if j > 1 else int(cur == needle[0])]
        if j == len(needle)
    ), None) if len(needle) else 0
