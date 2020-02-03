import multiprocessing
import time
import os

def slow_worker(n):
    #print('Starting worker')
    print('{}s passed...process_id:{}(pid:{})'.format(int(time.time()), n, os.getpid()))
    time.sleep(1)
    #print('Finished worker')

def job_sender(n, timeout, return_dict):
    start = time.time()
    cnt = 0
    while time.time() - start < timeout:
        slow_worker(cnt)
        cnt += 1
    return_dict[n] = cnt

def measure_throughput(processes, timeout):
    result_queue = multiprocessing.Queue()
    list_cnt = []
    list_que = []
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    for i in range(processes):
        list_que.append(multiprocessing.Process(target=job_sender, args=(i,timeout,return_dict)))
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
    print("Result count:", sum(list_cnt))
    print("Result throughput (1/sec):", sum(list_cnt)/timeout)

if __name__ == '__main__':
    measure_throughput(processes=100, timeout=5)
