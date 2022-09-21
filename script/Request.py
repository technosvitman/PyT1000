from .Sequence import Sequence

class Request(Sequence):
    def __init__(self, data):
        Sequence.__init__(self,data)
        self.__load(data)
    
    def __load(self, data):
        self.__period = data.get("period", 0)
        
    def __repr__(self):
        return 'Request ' + str(self)
    