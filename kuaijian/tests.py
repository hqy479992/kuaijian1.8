import time
from kuaijian.util.executor import Executor
from multiprocessing import Queue


def f(i1, q1):
    print(str(i1)+' start')
    time.sleep(2)
    q1.put(1)
    print(str(i1)+'end')

if __name__ == '__main__':
    e = Executor()
    for i in range(7):
        q = Queue()
        name = 'task-' + str(i)
        e.submit(name, q, f, i, q)
    for item in e.get_all_tasks():
        print(item)
        print(e.get_process(item))
    time.sleep(3)
    for item in e.get_all_tasks():
        print(item)
        print(e.get_process(item))
    time.sleep(3)
    for item in e.get_all_tasks():
        print(item)
        print(e.get_process(item))
