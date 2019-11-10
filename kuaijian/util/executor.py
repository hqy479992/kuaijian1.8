from multiprocessing import Process


class Executor:

    def __init__(self):
        self._tasks = {}
        self._queues = {}
        self._rate_cache = {}
        self._buffer = []

    def submit(self, task_name, queue, func, *args):
        if len(self._tasks) >= 4:
            print('{} add to cache'.format(task_name))
            self._rate_cache[task_name] = 0.0
            self._buffer.append((task_name, queue, func, args))
        else:
            p = Process(target=func, args=args)
            self._tasks[task_name] = p
            self._queues[task_name] = queue
            self._rate_cache[task_name] = 0.01
            print('start run task: {}'.format(task_name))
            p.start()

    def stop(self, task_name):
        if task_name in self._tasks:
            self._tasks[task_name].terminate()
            self._clean_infos(task_name)
            print("successful stopped task {}".format(task_name))
            if len(self._buffer) > 0:
                task_name, queue, func, args = self._buffer.pop(0)
                self.submit(task_name, queue, func, *args)
        else:
            del self._rate_cache[task_name]
            for item in self._buffer:
                if item[0] == task_name:
                    self._buffer.remove(item)
                    break

    def get_all_tasks(self):
        res = list(self._tasks.keys())
        res.extend([task[0] for task in self._buffer])
        return res

    def _clean_infos(self, task_name):
        del self._tasks[task_name]
        del self._queues[task_name]
        del self._rate_cache[task_name]

    def get_process(self, task_name):
        try:
            while True:
                rate = self._queues[task_name].get_nowait()
                self._rate_cache[task_name] = rate
        except:
            if len(self._buffer) > 0 and self._rate_cache[task_name] >= 1:
                self._clean_infos(task_name)
                task_name, queue, func, args = self._buffer.pop(0)
                self.submit(task_name, queue, func, *args)
            return self._rate_cache[task_name]
