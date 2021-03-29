import pickle

import numpy as np
from matplotlib import pyplot as plt
from tqdm.auto import tqdm

from scicomp.exam.kk import lzw_encode


digitss = pickle.load(open('pi/pi-bases.pickle', 'rb'))
cdigitss = {key: list(lzw_encode(val, set(val))) for key, val in tqdm(digitss.items())}

bases = np.array(list(digitss.keys()))
lens = np.array(list(map(len, digitss.values())))
cmaxs = np.array(list(map(max, cdigitss.values())))
clens = np.array(list(map(len, cdigitss.values())))
cclens = np.array(list(map(len, map(set, cdigitss.values()))))


plt.figure(figsize=(3.2, 2.6))
plt.plot(bases, np.log(cmaxs / cclens), '.')
plt.title(r'LZW encoding $\pi$')
plt.xlabel('base')
plt.ylabel('implicit information, nats')
plt.savefig('../_static/lzw-pi-bases.svg')
