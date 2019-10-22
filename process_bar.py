class ProcessBar:

    def __init__(self):
        self.__data = {'processed_length': 0, "total_length": 1,
                       }

    def set(self, key, value):
        self.__data[key] = value

    def get(self, key):
        return self.__data[key]

    def get_process(self):
        remainder = self.__data['_overall_view_remainder_length']
        total = self.__data['_overall_view_length']
        return round(1-(remainder/total), 2)
