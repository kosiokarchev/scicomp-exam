import pickle
from fractions import Fraction
from fractions import Fraction
from functools import partial
from math import floor, log
from multiprocessing import Pool

import numpy as np
from tqdm.auto import tqdm


def to_base(pi: Fraction, base):
    return base, [floor(ppi % base) for ppi in [pi] for i in range(int(log(pi.denominator) / log(base))) for ppi in [ppi * base]]


if __name__ == '__main__':
    obase = 10
    nodigits = 10_000
    pi = Fraction(int(open('pi').read()[2:][:nodigits]), obase**nodigits)

    bases = np.arange(2, 101, dtype=int).tolist()
    digitss = dict(tqdm(Pool().imap_unordered(partial(to_base, pi), bases), total=len(bases)))
    pickle.dump(digitss, open('pi-bases.pickle', 'wb'))
