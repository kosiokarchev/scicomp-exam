import math
from fractions import Fraction

import numpy as np
from more_itertools import always_reversible
from tqdm.auto import tqdm


modf = lambda x: (math.floor(x), x % 1)

pi = open('_pi/pi')
pi.seek(2)

# ndec = 1000
# nbatch = int(ndec / math.log10(42))
nbatch = 6142
base = Fraction(42)
basebatch = base ** nbatch

ndec = math.ceil(math.log10(basebatch.numerator) - math.log10(basebatch.denominator))
decbase = Fraction(10)**ndec
rat = Fraction(basebatch, decbase)


print(nbatch, ndec, float(basebatch / decbase))
digits = []

rem = 0
for i in tqdm(range(1_000_000 // ndec), unit_scale=nbatch):
    digit, rem = modf((rem + Fraction(int(pi.read(ndec)), decbase) * rat**i) * basebatch)
    if digit > basebatch:
        digits[-1] += digit // basebatch
    digits.extend((digit % base**j) // base**(j-1) for j in range(nbatch, 0, -1))
digits = np.array(digits, dtype=int)

for i, d in always_reversible(enumerate(digits)):
    if d >= base:
        digits[i-1], digits[i] = digits[i-1] + d // base, d % base
