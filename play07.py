from pebble import ProcessPool
from concurrent.futures import TimeoutError
import sys

def fibonacci(n):
    if n == 0: return 0
    elif n == 1: return 1
    else: return fibonacci(n - 1) + fibonacci(n - 2)

with ProcessPool() as pool:
    future = pool.map(fibonacci, range(50), timeout=10)

    try:
        for n in future.result():
            print(n)
    except TimeoutError:
        print("TimeoutError: aborting remaining computations")
        future.cancel()
        sys.exit()

