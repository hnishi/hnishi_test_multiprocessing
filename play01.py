# -*- coding: utf-8 -*-
from multiprocessing import Pool
import os
import time

start = time.time()

def f(x):
    time.sleep(1)
    value = x * x
    print('{}s passed...\t{}\t(pid:{})'.format(int(time.time() - start), value, os.getpid()))
    return value

with Pool(processes=2) as p:
    print(p.map(f, [1, 2]))


# コンテキストマネージャを使わずに以下のように書いても良い
# Pool(3).map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
