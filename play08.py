from multiprocessing import util, Pool, TimeoutError
from multiprocessing.dummy import Pool as ThreadPool
import threading
import sys
from functools import partial
import time
import os

start0 = time.time()

def worker(y):
    print("worker sleep {} sec, thread: {}".format(y, threading.current_thread()))
    print('{}s passed...\t{}\t(pid:{})'.format(int(time.time() - start0), y, os.getpid()))
    start = time.time()
    while True:
       if time.time() - start >= y:
           break
       time.sleep(0.5)
       # show work progress
       #print(y)
    return y


def collect_my_result(result):
    print("Got result {}".format(result))


def abortable_worker(func, *args, **kwargs):
    timeout = kwargs.get('timeout', None)
    p = ThreadPool(1)
    res = p.apply_async(func, args=args)
    try:
        # Wait timeout seconds for func to complete.
        out = res.get(timeout)
    except TimeoutError:
        print("Aborting due to timeout {}".format(args[1]))
        # kill worker itself when get TimeoutError
        sys.exit(1)
    else:
        return out


def empty_func():
    pass


if __name__ == "__main__":
    TIMEOUT = 4
    #util.log_to_stderr(util.DEBUG)
    pool = Pool(processes=4)

    # k - time to job sleep
    featureClass = [(k,) for k in range(20, 0, -1)]  # list of arguments
    for f in featureClass:
        # check available worker
        pool.apply(empty_func)

        # run job with timeout
        abortable_func = partial(abortable_worker, worker, timeout=TIMEOUT)
        pool.apply_async(abortable_func, args=f, callback=collect_my_result)

    time.sleep(TIMEOUT)
    pool.terminate()
    print("exit")
