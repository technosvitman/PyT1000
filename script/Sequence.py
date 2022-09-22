class Sequence():
            
    '''
        @brief init sequence
    '''
    def __init__(self):
        self.__seq = []
        self.__title = "NoName"
            
    '''
        @brief load sequence from yaml
        @param[IN] data yaml sequence representation
    '''
    def load(self, data):
        self.__seq = data.get("seq", [])
        self.__title = data.get("title", self.__title)
            
    '''
        @brief equality operator
    '''    
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
        
    '''
        @brief index operator
    '''    
    def __getitem__(self,key):
        return self.__seq[key]
        
    '''
        @brief len operator
    '''    
    def __len__(self):
        return len(self.__seq)
            
    '''
        @brief get title
        @return title
    '''
    def Title(self):
        return self.__title    
            
    '''
        @brief get sequence data
        @return sequence bytes
    '''
    def Seq(self):
        return self.__seq      
            
    '''
        @brief representation
        @return representation
    '''
    def __repr__(self):
        return 'Sequence ' + str(self)
            
    '''
        @brief string
        @return string
    '''
    def __str__(self):
        return '"%s" : %s'%(self.__title, str(self.__seq))
    