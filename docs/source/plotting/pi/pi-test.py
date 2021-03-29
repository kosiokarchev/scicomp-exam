import pickle
from fractions import Fraction
from math import floor, log

from tqdm.auto import tqdm

# from truth import truth as odigits
#
# nodigits = len(odigits)

odigits = open('pi').read()[2:]
nodigits = 10000

base = 42
obase = 10

ndigits = int(log(obase) / log(base) * nodigits) + 1

digits, rem = pickle.load(open('pi-42.pickle', 'rb'))

res = sum(d / Fraction(base**i) for i, d in tqdm(enumerate(digits[:ndigits], start=1), total=ndigits))
pred = floor(res * obase**nodigits)

print(str(pred)[:nodigits] == odigits[:nodigits])
