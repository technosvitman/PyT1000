import os
import sys
import datetime
import time
from datetime import datetime
import msvcrt
import threading

class Terminal(threading.Thread):
    def __init__(self, on_char):
        threading.Thread.__init__(self)
        self.__on_char = on_char
        self.start()        
        self.print("\033[2J")
    
    def run(self):
        output = ""
        while output != b"\x03":
            output = msvcrt.getch()
            self.__on_char(output)
                
        
    def print(self, str):
        print(str, end='')


class pyT1000(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.__last=time.time_ns()
        self.__quit=False
        self.__tagtime=False
        self.__term=None
        self.__prevdir = 0
        self.start()
        
    def run(self):
        while not self.__quit:
            if time.time_ns() - self.__last>1000000000:
                if not self.__tagtime:
                    self.__tagtime = True
                    self.__print("\n")
                    
        
    def setTerminal(self, terminal):
        self.__term = terminal
        
    def __print(self, str):
        if self.__term:
            self.__term.print(str)
        
    def __printtime(self, header):
        if self.__tagtime:
            self.__last = time.time_ns()
            if self.__term:
                self.__term.print(header+" ")
                self.__term.print(datetime.now().strftime("%H:%M:%S.%f"))
                self.__term.print(":\033[0m")
            self.__tagtime=False
                
        
    def onTx(self, char):
        if char == b"\x03":
            self.__quit=True
        else:
            #todo send
            if self.__prevdir == 0:
                self.__tagtime = True
                self.__print("\n")
                self.__prevdir=1
            self.__printtime("\n\033[32m TX")
            if int(char[0]) > 31 and int(char[0])<128:
                self.__print(char.decode())
            else:
                self.__print(str(char))
                        
    def onRx(self, char):
        if char == b"\x03":
            self.__quit=True
        else:
            if self.__prevdir == 1:
                self.__tagtime = True
                self.__print("\n")
                self.__prevdir=0
            self.__printtime("\n\033[33m RX")
            if int(char[0]) > 31 and int(char[0])<128:
                self.__print(char.decode())
            else:
                self.__print(str(char))
            
    

os.system("")
t1000 = pyT1000()
term = Terminal(t1000.onTx)
t1000.setTerminal(term)

data = b"pouet"
while t1000.is_alive():
    for d in data:
        t1000.onRx(d.to_bytes(1, "little"))
    time.sleep(1)

        