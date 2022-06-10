import datetime
import time
import argparse
from datetime import datetime
import threading
import keyboard
from core import *

class pyT1000(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.__last=time.time_ns()
        self.__quit=False
        self.__tagtime=False
        self.__term=None
        self.__prevdir = 0
        self.__ser=None
        self.__next_cmd=None
        self.__vtmode=False;
        self.__asciimode=False;
        keyboard.on_press_key(0x48, self.open_special)
        keyboard.on_press_key(0x4B, self.open_special)
        keyboard.on_press_key(0x4D, self.open_special)
        keyboard.on_press_key(0x50, self.open_special)
        self.start()
        
    def open(self, ser):
        self.__ser=ser
        self.__ser.open()
        
    def open_special(self, e):
        if self.__ser:
            k = e.scan_code
            if k == 0x48:
                self.__next_cmd = b"\033[A"
            elif k == 0x4B:
                self.__next_cmd = b"\033[B"
            elif k == 0x4D:
                self.__next_cmd = b"\033[C"
            elif k == 0x50:
                self.__next_cmd = b"\033[D"
        
    def close(self, ser):
        self.__ser.close()
        
    def setVtMode(self, vtmode=True):
        self.__vtmode=vtmode;
        
    def setAsciiMode(self, ascimode=True):
        self.__asciimode=ascimode;
        
    def run(self):
        while not self.__quit:
            if self.__ser:
                rdata = self.__ser.read(1)
                if rdata and rdata != b'':
                    if self.__vtmode:
                        self.__print(str(rdata, encoding='ansi'))
                    else:
                        self.onRx(rdata)
                if  self.__next_cmd:
                    self.__ser.write(self.__next_cmd)
                    self.__next_cmd=None
                
            if not self.__vtmode:
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
            
            
    def __printChar(self, char):
        if self.__asciimode :
            if int(char[0]) > 31 and int(char[0])<128:
                self.__print(char.decode())
            else:
                self.__print(str(char))
        else:
            self.__print("%02X "%int(char[0]))
        
                
        
    def onTx(self, char):
        if char == b"\x03":
            self.__quit=True
        else:
            if self.__ser:
                self.__ser.write(char)
            if not self.__vtmode:
                if self.__prevdir == 0:
                    self.__tagtime = True
                    self.__print("\n")
                    self.__prevdir=1
                self.__printtime("\n\033[32m TX")
                self.__printChar(char)
                        
    def onRx(self, char):
        if self.__prevdir == 1:
            self.__tagtime = True
            self.__print("\n")
            self.__prevdir=0
        self.__printtime("\n\033[33m RX")
        self.__printChar(char)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pyT1000 : complete serial terminal')
    parser.add_argument("-ascii", default=False, action="store_true")
    parser.add_argument("-vt100", default=False, action="store_true")
    
    args = parser.parse_args()

    t1000 = pyT1000()
    term = StdTerm(t1000.onTx)
    t1000.setTerminal(term)
    t1000.open(SerialCom("COM12", parity=PARITY_NONE))
    
    if args.vt100:
        t1000.setVtMode()
    elif args.ascii:
        t1000.setAsciiMode()
        
    while t1000.is_alive():
        time.sleep(1)

        