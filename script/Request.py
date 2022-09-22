from .Sequence import Sequence

class Request(Sequence):
    MIN_PERIOD = 10
    
    '''
        @brief init request sequence
    '''
    def __init__(self):
        Sequence.__init__(self)
        self.__period=0
    
    '''
        @brief load response from yaml
        @param[IN] data yaml response representation
    '''
    def load(self, data):
        Sequence.load(self, data)
        self.__period = data.get("period", 0)
        if self.__period<Request.MIN_PERIOD:
            self.__period = Request.MIN_PERIOD
            
    '''
        @brief get period
        @return period
    '''
    def Period(self):
        return self.__period 
            
    '''
        @brief representation
        @return representation
    '''
    def __repr__(self):
        return 'Request ' + str(self)
    