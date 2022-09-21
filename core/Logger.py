
class Logger():
    def __init__(self, filename):
        self.__f = open(filename,'w+')
        
    def print(self, str):
        print(str, end='', flush=True, file=self.__f)