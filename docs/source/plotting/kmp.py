from timeit import timeit

import matplotlib.pyplot as plt
import numpy as np
from more_itertools import first

from scicomp.exam.kk import kmp_search


FUNCS = {
    'kmp_search': lambda: kmp_search(needle, haystack),
    'native': lambda: haystack.find(needle),
    'naïve': lambda: first((i for i in range(len(haystack) - len(needle)) if haystack[i:i + len(needle)] == needle), None)
}


dt = []
n = np.logspace(1, 5, 81, dtype=int).tolist()
for i in n:
    N = int(1e6 / i)
    needle = i*'a'
    haystack = (i-1)*'a' + (i-1)*'b'

    dt.append([timeit(f, number=N) / N for f in FUNCS.values()])
    print(i, dt[-1])
dt = np.transpose(dt)

plt.figure(figsize=(4, 2.67))
plt.title('substring search runtimes')
for label, t in zip(FUNCS.keys(), dt):
    plt.loglog(n, t, label=label)
plt.legend()
plt.xlabel('length of needle = half length of haystack')
plt.ylabel('runtime per example, s')
plt.savefig('../_static/kmp.svg')
