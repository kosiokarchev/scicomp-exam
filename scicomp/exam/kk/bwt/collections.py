import bisect
from collections import UserList
from functools import cached_property
from operator import itemgetter
from typing import Iterable, TypeVar


_T = TypeVar('_T')
_K = TypeVar('_K')


class ReversibleList(UserList[_T]):
    def __reversed__(self) -> Iterable[_T]:
        i = 0
        while i+1 <= len(self):
            i += 1
            yield self.data[len(self) - i]


class PointedList(ReversibleList[_T]):
    """
    List that inserts at a particular location and moves that location forward
    or backward.
    """
    @cached_property
    def _pointer(self):
        return len(self)

    def insert_at_pointer(self, item: _T, offset=1):
        self._pointer = (self._pointer + offset,
                         self.insert(self._pointer, item))[0]

    def clear(self):
        super().clear()
        self._pointer = 0


class OrderedListDict(ReversibleList[tuple[_K, _T]]):
    """
    Rudimentary and inefficient implementation of a supposedly sorted
    "dictionary" as a list of ``(key, value)`` pairs. No guarantees are made!
    """

    def keys(self) -> Iterable[_K]:
        return map(itemgetter(0), self.data)

    def values(self) -> Iterable[_T]:
        return map(itemgetter(1), self.data)

    def items(self) -> Iterable[tuple[_K, _T]]:
        return self.data

    def __iter__(self) -> Iterable[tuple[_K, _T]]:
        return iter(self.data)

    def __contains__(self, item: _K):
        return item in self.keys()

    def __missing__(self, key):
        raise KeyError

    def __getitem__(self, item: _K) -> _T:
        try:
            return next(filter(lambda kv: kv[0] == item, self.data))[1]
        except StopIteration:
            pass
        return self.__missing__(item)

    def __setitem__(self, key: _K, value: _T):
        bisect.insort(self.data, (key, value))
