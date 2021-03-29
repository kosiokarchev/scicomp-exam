from collections import OrderedDict
from itertools import chain, islice
from operator import itemgetter
from typing import Callable, Iterable, Literal, Reversible, Sequence, TypeVar

from more_itertools import (always_reversible, consume, pairwise, prepend,
                            side_effect, stagger)

from .collections import OrderedListDict, PointedList
from .end_marker import _end_marker


__all__ = 'suffix_array',


_T = TypeVar('_T')
_K = TypeVar('_K')

_SL = Literal[0, 1, 2]
_SA_Bucket = OrderedDict[str, PointedList[int]]


class SABuckets(OrderedListDict[_K, _SA_Bucket]):
    default_factory = staticmethod(lambda: OrderedDict(L=PointedList(),
                                                       S=PointedList()))
    # To help static inspections...
    __getitem__: Callable[[_K], _SA_Bucket]
    values: Callable[[], Iterable[_SA_Bucket]]

    def __missing__(self, key):
        ret = self.default_factory()
        self[key] = ret
        return ret

    def __iter__(self) -> Iterable[int]:
        return self.iter_flat(super().__iter__())

    def __reversed__(self) -> Iterable[int]:
        return self.iter_flat(super().__reversed__(), reversed)

    @staticmethod
    def iter_flat(self, op=lambda x: x) -> Iterable[int]:
        return (i for k, b in self for v in op(b.values()) for i in op(v))

    def moditer(self, length):
        return map(lambda x: x % length, self)

    def __init__(self, seq: Sequence[_K], SL: Sequence[_SL], ssi: Iterable[int]):
        super().__init__()
        consume(chain(
            # tentatively put S*-suffixes in buckets:
            (self[seq[i]]['S'].insert_at_pointer(i) for i in ssi),
            # induce-sort L-suffixes:
            (self[seq[i - 1]]['L'].insert_at_pointer(i - 1)
             for i in self if not SL[i - 1]),
            # the S buckets need to be cleared and then repopulated:
            (b['S'].clear() for b in self.values()),
            # induce-sort S/S*-suffixes:
            (self[seq[i - 1]]['S'].insert_at_pointer(i - 1, offset=-1)
             for i in reversed(self) if SL[i - 1])
        ))


def get_SL(seq: Reversible) -> Iterable[_SL]:
    return (
        ret
        for prev in [True]
        for s in always_reversible(prepend(True, (
            S
            for nextS in [True]  # last is always S-type
            for nexts, s in stagger(reversed(seq), offsets=(0, 1))
            for S, nextS in [2*(s < nexts or (s == nexts and nextS),)]
        )))
        for ret in [s + (s and not prev)]  # S -> S* if prev == L, L -> L
        for prev in [s]
    )


def suffix_array(seq: Iterable[_T], assume_marked=False) -> Iterable[int]:
    """Calculate the suffix array (indices that sort the suffixes of `seq`)."""
    seq = seq if isinstance(seq, Sequence) else list(seq)

    if not (assume_marked or seq[-1] is _end_marker):
        seq.append(_end_marker)

    SL = list(get_SL(seq))
    ssi = list(filter(lambda i: SL[i] == 2, range(len(seq))))

    if len(ssi) > 1:
        ssi_o = list(filter(lambda i: SL[i] == 2,
                            SABuckets(seq, SL, ssi).moditer(len(seq))))

        # This is "cheating", but whatever. Since the indices of the S* are
        # sorted in ssi, we can use them to build a mapping that tells us where
        # a S*-substring ends, given its beginning, which is necessary for the
        # comparisons in the next step. Lookups in the mapping take linear time,
        # but we also do ~n lookups, so.... But we could have also implemented
        # a primitive sparse hasher like below to combat this with random
        # access, but we simply. won't. bother.
        ssp1p2 = {p1: p2+1 for p1, p2 in pairwise(chain(ssi, (len(seq),)))}

        inames = zip(ssi_o, chain((1,), (
            a for a in [1] for p1, p2 in pairwise(ssi_o)
            for p1p2, p2p2 in [(ssp1p2[p1], ssp1p2[p2])]
            for a in [a if seq[p1:p1p2] == seq[p2:p2p2] else a + 1]
        )))

        # Now re-sort according to original order. Rudimentary hash sorting
        # using a sparse array, but hey!, we're going for that O(n) time even
        # theoretically!
        names = len(seq)*[None]
        ssi = (list(ssi[i] for i in islice(suffix_array(  # recurse if needed
                  # Extract the names from sparse
                  list(filter(lambda x: x is not None, names))
               ), 1, None))
               # Distribute names across sparse, meanwhile finding the maximum
               # name, which indicates the number of distinct S*-suffixes.
               if (max(map(itemgetter(1),
                           side_effect(lambda iname: names.__setitem__(*iname),
                                       inames)))
                   < len(ssi))  # <- need to recurse
               else ssi_o)      # <- already sorted

    return SABuckets(seq, SL, ssi)
