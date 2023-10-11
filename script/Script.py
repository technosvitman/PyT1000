import yaml
from .Request import Request
from .RequestRunner import RequestRunner
from .Response import Response

class Script():

    '''
        @brief init script
    '''
    def __init__(self):    
        self.__on_auto_request = None
        self.__reqs=[]
        self.__runners=[]
        self.__resps=[]
        self.__buff=[]
        self.__maxseq=0
    '''
        @brief set on auto request
        @param[IN] on_auto_request on request send callback
    '''
    def setOnAutoRequest(self, on_auto_request):    
        self.__on_auto_request = on_auto_request
        
    '''
        @brief load script from file
        @param[IN] filename the file name
    '''
    def load(self, filename):
        f=open(filename, "r")
        root = yaml.load(f, Loader=yaml.FullLoader)
        reqs = root.get("reqs", [])
        resps = root.get("resps", [])
        for req in reqs:
            r=Request()
            r.load(req)
            self.__reqs.append(r)
            if r.Period():
                self.__runners.append(RequestRunner(r, self.onPeriod))
        for resp in resps:
            r=Response()
            r.load(resp)
            r.SetRunId(self.FindReq(r.Run()))
            s=len(r)
            if self.__maxseq < s:
                self.__maxseq = s
            self.__resps.append(r)
        
    '''
        @brief start runners for all request
    '''
    def start(self):
        for r in self.__runners:      
            r.start()
        
    '''
        @brief stop runners for all request
    '''
    def stop(self):
        for r in self.__runners:      
            r.stop()
        
    '''
        @brief on runner period hit
        @param[IN] runner the RequestRunner
        @param[IN] data the data sequence to send
    '''
    def onPeriod(self, runner, data):
        if self.__on_auto_request : 
            return self.__on_auto_request(data)
        return False
        
    '''
        @brief compute input data
        @return data to send or None
    '''
    def Compute(self, data):
        self.__buff.append(data)
        if len(self.__buff)>self.__maxseq:
            self.__buff.pop(0)
        for resp in self.__resps:
            if resp == self.__buff:
                self.__buff=[]
                return self.Run(resp.RunId())
        return None
        
    '''
        @brief compute key hit
        @return data to send or None
    '''
    def RunKey(self, key):        
        for req in self.__reqs:
            if req.Key() == key:
                return req.Seq()
        return None
        
    '''
        @brief find request
        @param[IN] title the request title
        @return request ID or none
    '''
    def FindReq(self, title):
        k=0
        for r in self.__reqs:
            if r == title :            
                return k
            k += 1
        return None
        
    '''
        @brief run request 
        @param[IN] id the request id
        @return data to send or None
    '''
    def Run(self, id):
        if id < len(self.__reqs):
            return self.__reqs[id].Seq()
        return None
        
    '''
        @brief string
        @return string
    '''
    def __str__(self):
        st = "Requests :"
        for req in self.__reqs:
            st += "\n\t"+str(req)
        st += "\nResponses :"
        for resp in self.__resps:
            st += "\n\t"+str(resp)
        return st
    