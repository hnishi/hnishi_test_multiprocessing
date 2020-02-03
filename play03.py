# -*- coding: utf-8 -*-
from multiprocessing import Pool
import os
import time
import pebble
from concurrent.futures import TimeoutError

start = time.time()

def f(x):
    time.sleep(1)
    value = x * x
    print('{}s passed...\t{}\t(pid:{})'.format(int(time.time() - start), value, os.getpid()))
    return value

timeout = time.time() + 10 # sec
while True:
    with pebble.ProcessPool(3) as p:
        task = p.schedule(f, args=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], timeout=5)
        try:
            result = task.get()
        except TimeoutError:
            print("Task: {} took more than 5 seconds to complete".format(task))




# コンテキストマネージャを使わずに以下のように書いても良い
# Pool(3).map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
