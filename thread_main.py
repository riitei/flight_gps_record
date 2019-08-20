import threading
from flightradar24_main import Flightradar24


class T_thread(threading.Thread):
    # airline_id = 中華航空 CI , 長榮航空 EVA , 中國國際航空 CA
    def __init__(self, airline_id,start_num,end_num):
        super().__init__()
        self.__airline_id = airline_id
        self.__start_num = start_num
        self.__end_num = end_num

    def run(self):
        f24 = Flightradar24()
        # f24.main('%s%d' % (self.__airline_id, i))
        for i in range(int(self.__start_num), self.__end_num):
            f24.main('%s%d' % (self.__airline_id, i))
            print('-- run -- %s%d --' % (self.__airline_id, i))
            f24.time_sleep(10)

if __name__ == "__main__":
    T_thread("BR", 1, 1000).start()
    T_thread("CA", 1, 2000).start()
    T_thread("CI", 1, 1000).start()
