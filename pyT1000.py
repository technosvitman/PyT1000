import datetime
import time
import argparse
import wx
from datetime import datetime
import threading
import keyboard
from core import *
from script import *
from gui import *

class pyT1000(threading.Thread):

    def __init__(self, outputdir, script):
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
        self.__logger = Logger(outputdir)
        self.__script=script
        
        keyboard.on_press_key(0x48, self.open_special)
        keyboard.on_press_key(0x4B, self.open_special)
        keyboard.on_press_key(0x4D, self.open_special)
        keyboard.on_press_key(0x50, self.open_special)
        keyboard.on_press_key(0x3B, self.open_special)
        keyboard.on_press_key(0x3C, self.open_special)
        keyboard.on_press_key(0x3D, self.open_special)
        keyboard.on_press_key(0x3E, self.open_special)
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
            elif k == 0x3B:
                self.__next_cmd = b"\033[P"
            elif k == 0x3C:
                self.__next_cmd = b"\033[Q"
            elif k == 0x3D:
                self.__next_cmd = b"\033[R"
            elif k == 0x3E:
                self.__next_cmd = b"\033[S"
        
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
                if  self.__next_cmd:
                    self.__ser.write(self.__next_cmd)
                    self.__next_cmd=None
                elif rdata and rdata != b'':
                    if self.__vtmode:
                        self.__print(str(rdata, encoding='ansi'))
                    else:
                        self.onRx(rdata)
                
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
        if not self.__vtmode:
            self.__logger.print(str)
        
    def __printtime(self, header):
        if self.__tagtime:
            self.__last = time.time_ns()
            self.__print(header+" "+
                        datetime.now().strftime("%H:%M:%S.%f") + ":\033[0m")
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
        elif not self.__next_cmd:
            if not self.__vtmode:
                if self.__prevdir == 0:
                    self.__tagtime = True
                    self.__print("\n")
                    self.__prevdir=1
                self.__printtime("\n\033[32m TX")
                self.__printChar(char)
            if self.__ser:
                self.__ser.write(char)
                        
    def onRx(self, char):
        if self.__prevdir == 1:
            self.__tagtime = True
            self.__print("\n")
            self.__prevdir=0
        self.__printtime("\n\033[33m RX")
        self.__printChar(char)
        if self.__script:
            dd=self.__script.Compute(char)
            if dd:
                d = bytes(dd)
                while len(d):
                    self.onTx(d[0:1])
                    d = d[1:]
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pyT1000 : complete serial terminal')
    parser.add_argument("-ascii", default=False, action="store_true")
    parser.add_argument("-vt100", default=False, action="store_true")
    parser.add_argument("-list", default=False, action="store_true")
    parser.add_argument("-gui", default=False, action="store_true")
    parser.add_argument("-s", type=str, default=None)
    parser.add_argument("-p", type=str, default=None)
    parser.add_argument("-L", type=str, default=".")
    parser.add_argument("-stp", choices=["STP1", "STP1_5", "STP2"], default="STP1")
    parser.add_argument("-par", choices=["NONE", "ODD", "EVEN"], default="NONE")
    parser.add_argument("-baud", type=int, default=115200)
    
    args = parser.parse_args()
    
    if args.list:
        print(SerialCom.list_ports())
        exit(0)
    
    if args.p:
        p=args.p
    else:
        p=SerialCom.list_ports()[0]
    s = SerialCom(p, 
                baudrate=args.baud,
                stopbits=SerialCom_Stop[args.stp],
                parity=SerialCom_Parity[args.par])  
    
    script=None
    if args.s:
        script = Script(args.s)
        print(script)

    t1000 = pyT1000(args.L, script)
    
    if args.gui:
        app = wx.App()
        frame = MainFrame()
        term = GuiTerm(t1000.onTx, frame.GetTerm())   
        t1000.setTerminal(term)
        t1000.open(s)
        app.SetTopWindow(frame)
        frame.Show()
        frame.Maximize(True)   
        app.MainLoop()
    else:    
        term = StdTerm(t1000.onTx)
        t1000.setTerminal(term)
        t1000.open(s)
    
        if args.vt100:
            t1000.setVtMode()
        elif args.ascii:
            t1000.setAsciiMode()
            
        while t1000.is_alive():
            time.sleep(1)

        