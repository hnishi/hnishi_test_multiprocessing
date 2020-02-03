import multiprocessing
import time
import os

start0 = time.time()

def slow_worker():
    cnt_req = 0
    print('Starting worker')
    print('{}s passed...(pid:{})'.format(int(time.time() - start0), os.getpid()))
    time.sleep(1)
    cnt_req += 1
    print('Finished worker')

def manager():
    cnt_req = 0
    while True:
        slow_worker()
        if time.time() - start0 >= 60:
            return 1

if __name__ == '__main__':
    list_que = []

    for _ in range(5):
        list_que.append(multiprocessing.Process(target=manager))
    for p in list_que:
        print('BEFORE:', p, p.is_alive())
        out = p.start()
        print("OUT", out)
        print('DURING:', p, p.is_alive())
    for p in list_que:
        p.join()
        p.terminate()
        print('TERMINATED:', p, p.is_alive())
        p.join()
        print('JOINED:', p, p.is_alive())
    #print("Result:", cnt_req)

