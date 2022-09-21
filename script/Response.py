from .Sequence import Sequence

class Response(Sequence):
    def __init__(self, data):
        Sequence.__init__(self,data)
        self.__load(data)
    
    def __load(self, data):
        self.__run = data.get("run", "")
        
    def Run(self):
        return self.__run    
        
    def __repr__(self):
        return 'Response ' + str(self)
    