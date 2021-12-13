import threading
import os
import random
from typing import Callable, Any

class SmartThreadPool:
    __max_avaiable_cpu = 0
    __threads = {}
    __thread_count = 0
    __uid = None

    def __init__(self):
        self.__max_avaiable_cpu = os.cpu_count() 
        if self.__max_avaiable_cpu == None or self.__max_avaiable_cpu == 0:
            raise CPUCountUnavaiableException("System doesn't provides CPU count so unable to adequately manage server threads")
        self.__uid = str(__import__('uuid').uuid4().hex)

    def new_thread(self, thread_target: Callable[[Any], None], *t_args, **t_kwargs) -> str:
        '''
        Создаёт и запускает новый поток и возвращает идентификатор, присвоенный данному потоку текущим экземпляром SmartThreadPool
        '''
        if self.__thread_count == self.__max_avaiable_cpu:
            raise MaxThreadsCountReachedException("Unable to create threads more than CPU threads")

        thread = threading.Thread(target = thread_target, args = t_args, kwargs = t_kwargs)
        thread.start()
        thread_uid = self.__uid + ':' + str(self.__thread_count)
        self.__threads[thread_uid] = thread;
        self.__thread_count += 1
        return thread_uid 

    def abort_thread(self, thread_uid: str, need_remove: bool = False) -> bool:
        if thread_uid in self.__threads.keys():
            if self.__threads[thread_uid].is_alive():
                self.__threads[thread_uid].join()   
                if need_remove:
                    del self.__threads[thread_uid]
                return True  
        return False

class CPUCountUnavaiableException(Exception):
    pass

class MaxThreadsCountReachedException(Exception):
    pass