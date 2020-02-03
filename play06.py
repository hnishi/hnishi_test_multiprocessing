import time
import os
import sys
from concurrent.futures import TimeoutError
from pebble import ProcessPool, ProcessExpired

start = time.time()

def function(n):
    time.sleep(1)
    print('{}s passed...\t{}\t(pid:{})'.format(int(time.time() - start), n, os.getpid()))
    return n

with ProcessPool() as pool:
    future = pool.map(function, range(100), timeout=10)

    iterator = future.result()

    while True:
        try:
            result = next(iterator)
        except StopIteration:
            break
        except TimeoutError as error:
            print("function took longer than %d seconds" % error.args[1])
            sys.exit()
            break
        except ProcessExpired as error:
            print("%s. Exit code: %d" % (error, error.exitcode))
            break
        except Exception as error:
            print("function raised %s" % error)
            print(error.traceback)  # Python's traceback of remote process
            break
