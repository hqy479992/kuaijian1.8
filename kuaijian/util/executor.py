from multiprocessing import Process


class Executor:

    def __init__(self):
        self.__tasks = {}

    def submit(self, task_name, func, *args):
        p = Process(target=func, args=args)
        self.__tasks[task_name] = p
        p.start()

    def stop(self, task_name):
        self.__tasks[task_name].terminate()
        print("successful stopped task {}".format(task_name))

    def get_process(self, task_name):
        self.__tasks[task_name].get_process()
