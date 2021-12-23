import threading
import os
import random
from datetime import datetime
from typing import Callable, Any

class SmartThreadPool:
    __max_avaiable_cpu = 0
    __threads = {}
    __threads_err = {}
    __threads_pulse = {}
    __thread_count = 0 #Данный счётчик означает общее кол-во потоков, когда либо созданных в текущем экземпляре SmartThreadPool, а не кол-во активных потоков. Кол-во активных потоков см. св-во active_threads_count
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
        if len(self.__threads.keys()) == self.__max_avaiable_cpu:
            raise MaxThreadsCountReachedException("Unable to create threads more than CPU threads")
        thread_uid = self.__uid + ':' + str(self.__thread_count)
        self.__threads_pulse[thread_uid] = str(datetime.now())#пульс из треда не доступен удоли
        t_kwargs['err_list'] = self.__threads_err
        t_kwargs['host_id'] = thread_uid
        t_kwargs['host_pulse'] = self.__threads_pulse

        thread = threading.Thread(target = thread_target, args = t_args, kwargs = t_kwargs)
        thread.start()
        
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

    def killAll(self):
        for i in __threads.keys():
            abort_thread(i)

    @property
    def active_threads_count(self):
        return len(self.__threads.keys())

    @property
    def threads_list(self):
        reply = {}
        for key in self.__threads.keys():
            reply[key] = {f"status: {('alive' if self.__threads[key].is_alive() else 'dead')}"}
        return reply

    @property
    def threads_err(self):
        return self.__threads_err

    @property
    def threads_pulses(self):
        return self.__threads_pulse


class CPUCountUnavaiableException(Exception):
    pass

class MaxThreadsCountReachedException(Exception):
    pass