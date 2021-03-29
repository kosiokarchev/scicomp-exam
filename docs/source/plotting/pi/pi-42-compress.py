import pickle
from functools import partial
from multiprocessing import Pool

import numpy as np
from more_itertools import ilen
from tqdm.auto import tqdm

from scicomp.exam.kk import lzw_encode


_alphabet = list(range(42))


def compress_one(n, digits):
    return n, ilen(lzw_encode(digits[:n], _alphabet))


if __name__ == '__main__':
    digits = np.load('pi/pi-42.npy')[:500_000]
    n = [2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000,
         10_000, 20_000, 50_000, 100_000, 200_000, 500_000]

    compressions = list(tqdm(Pool().imap_unordered(partial(compress_one, digits=digits), n), total=len(n)))
    pickle.dump(compressions, open('pi-42-compressions.pickle', 'wb'))
