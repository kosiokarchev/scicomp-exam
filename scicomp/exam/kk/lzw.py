from itertools import repeat, takewhile
from typing import Iterable, Sequence, TypeVar

from more_itertools import always_iterable, collapse, first, stagger


__all__ = 'lzw_encode', 'lzw_decode'


_T = TypeVar('_T')


def lzw_encode(seq: Sequence[_T], alphabet: Iterable[_T]) -> Iterable[int]:
    """Encode a sequence using the `Lempel–Ziv–Welch algorithm
    <https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch>`_.

    Args:
        seq: the sequence to encode.
        alphabet: a collection of possible unique elements in `seq`. If you
            don't know the alphabet, go back to  first grade, or get it via
            ``set(seq)``.

    Returns:

        The LZW encoding of `seq` as an iterable of indices into an ordered
        "bag" that starts off with just the alphabet and is dynamically built.

    Warnings:
        Returns an iterator, so make sure to "consume" it before e.g. saving,
        or if you plan to re-use the result.

    See Also:
        `lzw_decode`
    """
    bag = list(map(tuple, map(always_iterable, alphabet)))
    return (
        # Advance sequence, add element to bag, record index in output
        (seq := seq[len(s):], bag.append((*s, next(iter(seq), None))), i)[-1]
        # while loop
        for _ in takewhile(lambda x: len(seq), repeat(None))
        # Find the longest element in the bag that matches at the current
        # position. Guaranteed to find at least one match if all elements are
        # in the original alphabet. I don't check the other case.
        for res in [first((
            (bag.index(sub), sub)
            for j in range(2, len(seq)+1)
            for sub in [tuple(seq[:j])] if sub not in bag for sub in [sub[:-1]]
        ), None)]  # if this failed, then seq must be in the bag already!
        for i, s in [res if res is not None else (bag.index(tuple(seq)), seq)]
    )


def lzw_decode(idx: Iterable[int], alphabet: Sequence[_T]) -> Iterable[_T]:
    """Decode a sequence previously encoded using `lzw_encode`.

    Args:
        idx: the output of `lzw_encode`, being an iterable of indices into a
            bag of elements.
        alphabet: the alphabet used to encode. This has to be the same as
            the one passed to `lzw_encode`: no more, no fewer elements, in the
            same order, otherwise gibberish will ensue!

    Returns:

        The decoded sequence. It is generally not of the same object type as
        the original, though, so care should be taken to do item-by-item
        comparison, especially with strings, which get decoded into an
        iterator of length-one strings (characters).

    Warnings:
        Returns an iterator, so make sure to "consume" it before e.g. saving,
        or if you plan to re-use the result.

    See Also:
        `lzw_encode`
    """
    bag = list(map(tuple, map(always_iterable, alphabet)))
    return collapse((  # bag elements are tuples, so unpack them
        bag[i]
        for i, nexti in stagger(idx, offsets=(0, 1), longest=True)
        for _ in [
            bag.append((
                *bag[i], next(iter(bag[nexti] if len(bag) > nexti else bag[i]))
            )) if nexti is not None else None]
    ), levels=1)
