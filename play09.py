import multiprocessing
import time
import os

start0 = time.time()

def slow_worker(n):
    print('Starting worker')
    print('{}s passed...process_id:{}(pid:{})'.format(int(time.time() - start0), n, os.getpid()))
    time.sleep(1)
    print('Finished worker')

if __name__ == '__main__':
    cnt_req = 0
    while True:
        list_que = []
        for _ in range(5):
            list_que.append(multiprocessing.Process(target=slow_worker, args=('bob',)))
        for p in list_que:
            print('BEFORE:', p, p.is_alive())
            p.start()
            print('DURING:', p, p.is_alive())
        for p in list_que:
            p.join()
            p.terminate()
            print('TERMINATED:', p, p.is_alive())
            p.join()
            print('JOINED:', p, p.is_alive())
            cnt_req += 1
            if time.time() - start0 >= 5:
                break
        else:
            continue
        break
    print("Result:", cnt_req)

