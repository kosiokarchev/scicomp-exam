from itertools import repeat, takewhile, tee
from typing import Iterator, Sequence, TypeVar

from more_itertools import zip_offset


_T = TypeVar('_T')


def lzw_encode(seq: Sequence[_T], alphabet: Sequence[_T] = None) -> list[int]:
    bag = list(map(tuple, alphabet))
    return [
        (seq := seq[len(s):], bag.append((*s, next(iter(seq), None))), i)[-1]
        for _ in takewhile(lambda x: len(seq), repeat(None))  # while loop
        for i, s in [max(((i, s) for i, s in enumerate(bag) if len(s) <= len(seq) and all(a == b for a, b in zip(seq, s))), key=lambda i_s: len(i_s[1]))]
    ]


def lzw_decode(idx: Iterator[int], alphabet: Sequence[_T]) -> Iterator[_T]:
    bag = list(map(tuple, alphabet))
    return (
        bag[i]
        for i, nexti in zip_offset(*tee(idx), offsets=(0, 1), longest=True)
        for _ in [bag.append((*bag[i], next(iter(bag[nexti] if len(bag) > nexti else bag[i])))) if nexti is not None else None]
    )
