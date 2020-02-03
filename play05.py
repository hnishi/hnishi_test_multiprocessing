from pebble import concurrent
import time
import os

start = time.time()

@concurrent.process
def function(arg, kwarg=0):
    time.sleep(1)
    print('{}s passed...\t{}\t(pid:{})'.format(int(time.time() - start), kwarg, os.getpid()))
    return arg, kwarg

future = function(1, kwarg=1)
print(future.result())

