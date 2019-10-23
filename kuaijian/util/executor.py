from kuaijian.util.process_x import ClipProcess


class Executor:

    def __init__(self):
        self.__tasks = {}

    def submit(self, task_name, cls, *args):
        p = ClipProcess(cls, *args)
        self.__tasks[task_name] = p
        p.start()

    def stop(self, task_name):
        self.__tasks[task_name].terminate()
        inner_class = self.__tasks[task_name].get_inner_class()
        del inner_class
        print("successful stopped task {}".format(task_name))

    def get_process(self, task_name):
        return self.__tasks[task_name].get_process()
