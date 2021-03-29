import string
import timeit
from functools import partial
from multiprocessing import Pool
from random import choices, randint

import numpy as np
from matplotlib import pyplot as plt
from more_itertools import circular_shifts, ilen, last
from tqdm import tqdm

from scicomp.exam.kk import bwt_encode, lzw_encode


_alphabet = string.ascii_lowercase


def random_string(length, alph=_alphabet):
    return ''.join(choices(alph, k=length))


def do_one(s, alph=_alphabet):
    if not isinstance(s, str):
        s = random_string(s, alph)
    return (
        ilen(lzw_encode(s, alph)),
        ilen(lzw_encode(list(filter(lambda c: isinstance(c, str), bwt_encode(s))), alph))
    )


if __name__ == '__main__':
    # lengths = [10, 20, 50, 100, 200, 500, 1000, 2000,
    #            5000, 10_000, 20_000]
    # times = np.array([[[
    #     timeit.timeit(lambda: list(func(s)), number=1) for func in (
    #         bwt_encode, lambda seq: map(last, sorted(circular_shifts(s + '\0')))
    #     )]
    #     for i in range(10)
    #     for s in [random_string(length)]
    # ] for length in lengths for _ in [print(length)]])
    #
    # plt.figure(figsize=(3.5, 2.6))
    # plt.title('BWT algorithms')
    # for y, pwr, name, o in zip(times.mean(-2).T, (1, 2), ('SA', 'naïve'), ('n', 'n^2')):
    #     plt.loglog(lengths, y[-1] * (np.array(lengths) / lengths[-1])**pwr, '--', c=plt.loglog(lengths, y, label=f'{name} $O({o})$')[0].get_color())
    # plt.legend()
    # plt.xlabel('n')
    # plt.ylabel('runtime, s')
    # plt.savefig('../_static/bwt-runtime.svg')

    lens = (np.random.random(size=1000) * 10000).astype(int)

    oclens, bwtclens = np.transpose(list(tqdm(Pool().imap_unordered(
        partial(do_one), lens), total=len(lens))))
    plt.plot(lens, bwtclens / oclens, '.', label='random')

    h2g2 = open('h2g2.txt').read().lower()

    oclens, bwtclens = np.transpose(list(tqdm(Pool().imap_unordered(
        partial(do_one, alph=set(h2g2)), (h2g2[randint(0, len(h2g2)-l):][:l] for l in lens)), total=len(lens))))
    plt.plot(lens, bwtclens / oclens, '.', label=r'$\mathrm{H}^2 \mathrm{G}^2$')

    plt.gcf().set_size_inches((3.5, 2.6))
    plt.legend(loc='lower center', ncol=2)
    plt.title('LZW compressing BWT')
    plt.xlabel('string length')
    plt.ylabel('BWT / original compressed size')
    plt.ylim(0.9, 1.15)
    plt.savefig('../_static/bwt-compression.svg')
