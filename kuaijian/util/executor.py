from multiprocessing import Process


class Executor:

    def __init__(self):
        self._tasks = {}
        self._queues = {}

    def submit(self, task_name, queue, func, *args):
        p = Process(target=func, args=args)
        self._tasks[task_name] = p
        self._queues[task_name] = queue
        p.start()

    def stop(self, task_name):
        self._tasks[task_name].terminate()
        del self._tasks[task_name]
        del self._queues[task_name]
        print("successful stopped task {}".format(task_name))

    def get_process(self, task_name):
        pass

    def get_all_tasks(self):
        return list(self._tasks.keys())

    def get_process(self, task_name):
        try:
            return self._queues[task_name].get(timeout=1)
        except:
            return 0.01
