from typing import Iterable, Optional, Sequence, TypeVar


__all__ = 'kmp_search',


_T = TypeVar('_T')


def _kmp_table(needle: Sequence[_T]) -> Sequence[int]:
    """Compute the KMP partial match "table"."""
    return [j for j in [-1]
            for cur in needle  # linear scan of the needle
            for j in [j+1 if cur == needle[j] else 0]]


def kmp_search(needle: Sequence[_T], haystack: Iterable[_T]) -> Optional[int]:
    """
    Find the first occurence of `needle` in `haystack` using the `KMP algorithm
    <https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm>`_.

    Args:
        needle: subsequence to search for
        haystack: sequence to search in

    Returns:

        The index of the first occurence of `needle` in `haystack` or
        `None` if not found. In general  (unless `None`, of course),::

            haystack[kmp_search(needle, haystack):][:len(needle)] == needle

        which means that, like the builtin `index <str.index>` /
        `find <str.find>` methods of Python strings, for an empty `needle`,
        this returns ``0``.

    Notes:
        Since random access into the `needle` is needed, it is required to be a
        sequence. The `haystack` on the other hand can be any iterable.

        Comparison is performed using `== <object.__eq__>`, so the usual
        equality rules apply.
    """
    return next((
        i-j+1

        for tbl, j in [(_kmp_table(needle), 0)]  # initialise

        # indeed, cycle only once through haystack!:
        for i, cur in enumerate(haystack)

        # checks here allow the table building to be slightly simpler
        # and to allow a non-sequence iterable haystack
        for j in [(j if needle[j] == cur else tbl[j-1] if j > 0 else -1) + 1]

        # if starting all over, check current against the first:
        for j in [j if j > 1 else int(cur == needle[0])]
        if j == len(needle)  # breaking condition
    ), None) if len(needle) else 0
