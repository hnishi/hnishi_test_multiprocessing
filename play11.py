import multiprocessing
import time
import os

start = time.time()

def slow_worker(n):
    print('Starting worker')
    print('{}s passed...process_id:{}(pid:{})'.format(int(time.time() - start), n, os.getpid()))
    time.sleep(1)
    print('Finished worker')

def job_sender(n, return_dict):
    cnt = 0
    while time.time() - start < 5:
        slow_worker(cnt)
        cnt += 1
    return_dict[n] = cnt

if __name__ == '__main__':
    result_queue = multiprocessing.Queue()
    list_cnt = []
    list_que = []
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    for i in range(100):
        list_que.append(multiprocessing.Process(target=job_sender, args=(i,return_dict)))
    for p in list_que:
        print('BEFORE:', p, p.is_alive())
        p.start()
        print('DURING:', p, p.is_alive())
    for i, p in enumerate(list_que):
        p.join()
        p.terminate()
        print('TERMINATED:', p, p.is_alive())
        p.join()
        print('JOINED:', p, p.is_alive())
        list_cnt.append(return_dict[i])
    print("Result:", sum(list_cnt))

