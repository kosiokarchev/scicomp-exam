from typing import Iterable, Optional, Sequence, TypeVar


_T = TypeVar('_T')


def _kmp_table(needle: Sequence[_T]) -> Sequence[int]:
    """Compute the KMP partial match "table"."""
    return [j for j in [-1]
            for cur in needle  # linear scan of the needle
            for j in [j+1 if cur == needle[j] else 0]]


def kmp_search(needle: Sequence[_T], haystack: Iterable[_T]) -> Optional[int]:
    """
    Find the first occurence of `needle` in `haystack`.

    Args:
        needle: subsequence to search form
        haystack: sequence to search in

    Returns:
        The index of the first occurence of `needle` in `haystack` or `None` if
            not found. In general,::

                haystack[kmp_search(needle, haystack):][:len(needle)] == needle

            which means that, like the builtin `index`/`find` methods, for an
            empty `needle`, this returns ``0``.
    """
    t = _kmp_table(needle)
    return next((
        i-j+1
        for j in [0]  # initialise

        # indeed, cycle only once through haystack!:
        for i, cur in enumerate(haystack)

        # checks here allow the table building to be slightly simpler
        # and to allow a non-sequence iterable haystack
        for j in [(j if needle[j] == cur else t[j-1] if j > 0 else -1) + 1]

        # if starting all over, check current against the first:
        for j in [j if j > 1 else int(cur == needle[0])]
        if j == len(needle)  # breaking condition
    ), None) if len(needle) else 0
