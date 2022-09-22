from .Sequence import Sequence

class Response(Sequence):
            
    '''
        @brief init response sequence
    '''
    def __init__(self):
        Sequence.__init__(self)
        self.__run = ""
        self.__runid = None
    
    '''
        @brief load response from yaml
        @param[IN] data yaml response representation
    '''
    def load(self, data):
        Sequence.load(self, data)
        self.__run = data.get("run", "")
            
    '''
        @brief get run target
        @return run
    '''
    def Run(self):
        return self.__run 
            
    '''
        @brief set run ID
        @param[IN] id the run id
    '''
    def SetRunId(self, id):
        self.__runid = id 
            
    '''
        @brief get run ID
        @return run ID
    '''
    def RunId(self):
        return self.__runid
            
    '''
        @brief representation
        @return representation
    '''
    def __repr__(self):
        return 'Response ' + str(self)
    