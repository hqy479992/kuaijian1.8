from multiprocessing import Process


class ClipProcess(Process):

    def __init__(self, clip_cls, *args):
        self.__clip_cls = clip_cls
        self.__params = args
        self.__clip_controller = self.__clip_cls(*self.__params)
        Process.__init__(self)

    def run(self) -> None:
        self.__clip_controller.run()

    def get_process(self):
        print(dir(self.__clip_controller))
        return self.__clip_controller.get_process()

    def get_inner_class(self):
        return self.__clip_controller
