class Sequence():
    def __init__(self, data):
        self.__load(data)
    
    def __load(self, data):
        self.__seq = data.get("seq", [])
        self.__title = data.get("title", "Noname")
        
    def __eq__(self, other):
        if isinstance(other, str):
            return self.__title == other
        elif isinstance(other, list):
            s = len(self)
            if s > len(other) :
                return False
            j = 0
            while self[0] != other[j]:
                j += 1
                if j == len(other) or (j+s) > len(other):
                    return False
            for i in range(0, s):
                if self[i] != other[j+i] :
                    return False
            return True
        return False
        
    def __getitem__(self,key):
        return self.__seq[key]
        
    def __len__(self):
        return len(self.__seq)
        
    def Title(self):
        return self.__title    
        
    def Seq(self):
        return self.__seq               
        
    def __repr__(self):
        return 'Sequence ' + str(self)
        
    def __str__(self):
        return '"%s" : %s'%(self.__title, str(self.__seq))
    