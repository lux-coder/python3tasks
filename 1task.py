from multiprocessing import Process
from multiprocessing import Lock
from multiprocessing import current_process
from time import sleep
import logging


class ProcessLog:
    
    def __init__(self):    
        self.logger = logging.getLogger()
        formatter = logging.Formatter("%(asctime)s:%(message)s")    
        self.logger.setLevel(logging.INFO)    
        self.process_name = '%s' % current_process().name    
        filename = '{}.log'.format(str(self.process_name))
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
class MyProcess(ProcessLog):    
    logging.basicConfig(level=logging.INFO, filename="CentralLog.log", 
                        format="%(asctime)s:%(message)s")
    
    def __init__(self,s, lock):
        Process(target=self.printit, args=(s, lock,)).start()
    
    def printit(self, s, lock):
        ProcessLog.__init__(self)
        while True:
            lock.acquire()
            try:
                self.logger.info(self.process_name)                
                sleep(s)
            finally:
                lock.release()
                
if __name__ == '__main__':
    lock = Lock()
    sleepTime = [5, 0.2, 2]
    for s in sleepTime:
        MyProcess(s, lock)