from datetime import datetime

class Logger():
    LOG_TIMEOUT=300
    def __init__(self, directory):
        self.__dir=directory
        self.__f=None
        self.__start()
        
    def __start(self):    
        if self.__f:
            self.__f.close()
        self.__date = datetime.now()        
        self.__f = open(self.__dir+"/log_%s.txt"%self.__date.strftime("%Y%m%d_%H%M%S"),'w+')
        
    def print(self, str):
        dd = datetime.now() - self.__date
        if dd.total_seconds() > Logger.LOG_TIMEOUT:
            self.__start()
        print(str, end='', flush=True, file=self.__f)