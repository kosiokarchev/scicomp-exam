from functools import total_ordering


@total_ordering
class EndMarker:
    def __repr__(self):
        return '$'

    def __lt__(self, other):
        return True


_end_marker = EndMarker()
