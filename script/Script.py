import yaml
from .Request import Request
from .Response import Response

class Script():
    def __init__(self, filename):
        self.__reqs=[]
        self.__resps=[]
        self.__buff=[]
        self.__maxseq=0
        self.__load(filename)
    
    def __load(self, filename):
        f=open(filename, "r")
        root = yaml.load(f, Loader=yaml.FullLoader)
        reqs = root.get("reqs", [])
        resps = root.get("resps", [])
        for req in reqs:
            r=Request()
            r.load(req)
            self.__reqs.append(r)
        for resp in resps:
            r=Response()
            r.load(resp)
            s=len(r)
            if self.__maxseq < s:
                self.__maxseq = s
            self.__resps.append(r)        
    
    def Compute(self, data):
        self.__buff += data
        if len(self.__buff)>self.__maxseq:
            self.__buff.pop(0)
        for resp in self.__resps:
            if resp == self.__buff:
                self.__buff=[]
                return self.Run(resp.Run())
        return None
    
    def Run(self, title):
        for r in self.__reqs:
            if r == title :
                return r.Seq()
        return None
            
    def __str__(self):
        st = "Requests :"
        for req in self.__reqs:
            st += "\n\t"+str(req)
        st += "\nResponses :"
        for resp in self.__resps:
            st += "\n\t"+str(resp)
        return st
    