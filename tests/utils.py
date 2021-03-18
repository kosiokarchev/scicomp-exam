import string
from itertools import repeat
from random import choices, randint


_alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits


def _get_random_string(length):
    return ''.join(choices(_alphabet, k=length))


def random_strings(min_length, max_length=None, N=None):
    return (
        _get_random_string(randint(min_length, max_length)
                           if max_length else min_length)
        for _ in (range if N is not None else repeat)(N)
    )
