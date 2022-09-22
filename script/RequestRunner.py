import threading
import time

class RequestRunner(threading.Thread):
    
    '''
        @brief init request runner
        @param[IN] request the request to run
        @param[IN] on_period on period elapsed
        
    '''
    def __init__(self, request, on_period):
        threading.Thread.__init__(self)
        self.__req=request
        self.__on_period=on_period
    
    '''
        @brief task
    '''
    def run(self):
        while True:
            time.sleep(self.__req.Period()/1000)
            if not self.__on_period(self, self.__req.Seq()) : 
                return