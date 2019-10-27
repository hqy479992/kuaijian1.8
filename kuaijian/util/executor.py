from multiprocessing import Process


class Executor:

    def __init__(self):
        self.__tasks = {}
        self.__process_bars = {}

    def submit(self, task_name, process_bar, func, *args):
        p = Process(target=func, args=args)
        self.__tasks[task_name] = p
        self.__process_bars[task_name] = process_bar
        p.start()

    def stop(self, task_name):
        self.__tasks[task_name].terminate()
        del self.__tasks[task_name]
        del self.__process_bars[task_name]
        print("successful stopped task {}".format(task_name))

    def get_process(self, task_name):
        return self.__process_bars[task_name].get_process()

    def get_all_tasks(self):
        return list(self.__tasks.keys())
