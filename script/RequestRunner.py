import threading
import time

class RequestRunner(threading.Thread):
    
    '''
        @brief init request runner
        @param[IN] request the request to run
        @param[IN] on_period on period elapsed
        
    '''
    def __init__(self, request, delay, on_period):
        threading.Thread.__init__(self)
        self.__req=request
        self.__on_period=on_period
        self.__delay=delay
    
    '''
        @brief task
    '''
    def run(self):
        while True:
            if self.__req.Period() : 
                time.sleep(self.__req.Period()/1000)
                if not self.__on_period or not self.__on_period(self, self.__req) : 
                    return
            if self.__delay : 
                time.sleep(self.__delay/1000)
                self.__on_period(self, self.__req, True)
                return
    
    '''
        @brief stop
    '''
    def stop(self):        
        self.__on_period=None