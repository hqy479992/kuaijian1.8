from multiprocessing import Process


class ClipProcess(Process):

    def __init__(self, clip_controller):
        self.__clip_controller = clip_controller
        Process.__init__(self)

    def run(self) -> None:
        self.__clip_controller.run()
        del self.__clip_controller

    def get_process(self):
        return self.__clip_controller.get_process()

    def get_inner_class(self):
        return self.__clip_controller
