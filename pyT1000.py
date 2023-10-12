import datetime
import time
import argparse
from datetime import datetime
import threading
import keyboard
from core import *
from script import *

class pyT1000(threading.Thread):

    TX_COLOR = "\033[32m"
    RX_COLOR = "\033[33m"
    SEQ_COLOR = "\033[96m"
    INFO_COLOR = "\033[36m"
    NORMAL_COLOR = "\033[37;40m"

    '''
        @brief init pyT1000
        @param[IN] outputdir log file output directory
        @param[IN] script loaded script
    '''
    def __init__(self, outputdir, script):
        threading.Thread.__init__(self)
        self.__last=time.time_ns()
        self.__quit=False
        self.__tagtime=False
        self.__term=None
        self.__prevdir = 0
        self.__ser=None
        self.__next_cmd=None
        self.__skip=0
        self.__vtmode=False;
        self.__asciimode=False;
        self.__logger = Logger(outputdir)
        self.__script=script
        
        keyboard.on_press_key(0x48, self.on_special)
        keyboard.on_press_key(0x4B, self.on_special)
        keyboard.on_press_key(0x4D, self.on_special)
        keyboard.on_press_key(0x50, self.on_special)
        # F1
        keyboard.on_press_key(0x3B, self.on_special)
        # F2
        keyboard.on_press_key(0x3C, self.on_special)
        # F3
        keyboard.on_press_key(0x3D, self.on_special)
        # F4
        keyboard.on_press_key(0x3E, self.on_special)
        # F5
        keyboard.on_press_key(0x3F, self.on_special)
        # F6
        keyboard.on_press_key(0x40, self.on_special)
        # F7
        keyboard.on_press_key(0x41, self.on_special)
        # F8
        keyboard.on_press_key(0x42, self.on_special)
        # F9
        keyboard.on_press_key(0x43, self.on_special)
        # F10
        keyboard.on_press_key(0x44, self.on_special)
        # F11
        keyboard.on_press_key(0x45, self.on_special)
        # F12
        keyboard.on_press_key(0x46, self.on_special)
        self.start()   
        if script:
            script.setOnAutoRequest(self.onScriptPeriod)
            script.start()

    '''
        @brief open serial port
        @param[IN] ser SerialCom to open
    '''
    def open(self, ser):
        self.__ser=ser
        self.__ser.open()        

    '''
        @brief on special key event
        @param[IN] e the key event
    '''
    def on_special(self, e):
        k = e.scan_code
        self.__skip  = 1
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
        elif k >= 0x3F and k <= 0x42:
            if self.__script : 
                tt, self.__next_cmd = self.__script.RunKey(k-0x3E)
                if not self.__vtmode:  
                    if self.__next_cmd :                   
                        self.__tagtime = True              
                        self.__printtime("\n"+self.INFO_COLOR+"MANUAL : "+self.SEQ_COLOR+tt+"\n"+self.TX_COLOR+" TX")                    
                        for d in self.__next_cmd : 
                            self.__printChar(d)
                        self.__tagtime = True
                        
        elif k == 0x44:
            self.__print("\r\n\033[31m EXIT!" + self.NORMAL_COLOR)
            self.__term.close()
            if script:
                script.stop()
            time.sleep(1)
            self.__quit = True

    '''
        @brief close serial port
    '''
    def close(self):
        self.__ser.close()
    
    '''
        @brief enable/disable VT100 mode
        @param[IN] vtmode if true enable VT100
    '''   
    def setVtMode(self, vtmode=True):
        self.__vtmode=vtmode;
    
    '''
        @brief enable/disable ASCII mode
        @param[IN] asciimode if true enable ASCII mode
    '''
    def setAsciiMode(self, asciimode=True):
        self.__asciimode=asciimode;
       

    '''
        @brief pyT1000 task
    ''' 
    def run(self):
        while not self.__quit:
            if self.__ser:
                rdata = self.__ser.read(10)
                if  self.__next_cmd:
                    self.__ser.write(self.__next_cmd)
                    self.__next_cmd = None
                if rdata and rdata != b'':
                    for d in rdata : 
                        if self.__vtmode:
                            self.__print(chr(d))
                        else:
                            self.__onrx(d)
                
            if not self.__vtmode:
                if time.time_ns() - self.__last>1000000000:
                    if not self.__tagtime:
                        self.__tagtime = True
        self.__term.close()
        self.__print("\033[m\033[2J\033[H")
        exit(0)
        

    '''
        @brief define terminal used
        @param[IN] terminal the Terminal
    '''
    def setTerminal(self, terminal):
        self.__term = terminal

    '''
        @brief print method, output to log and terminal
        @param[IN] str the string to print
    ''' 
    def __print(self, str):
        if self.__term:
            self.__term.print(str)
        if not self.__vtmode:
            self.__logger.print(str)
       

    '''
        @brief print time to output
        @param[IN] header the header to print befor time
    ''' 
    def __printtime(self, header):
        if self.__tagtime:
            self.__last = time.time_ns()
            self.__print(header+" "+
                        datetime.now().strftime("%H:%M:%S.%f") + ":" + self.NORMAL_COLOR)
            self.__tagtime=False
            
       

    '''
        @brief print byte to output
        @param[IN] char the byte to output
    '''     
    def __printChar(self, char):
        if self.__asciimode :
            if int(char) > 31 and int(char)<128:
                self.__print(chr(char))
            else:
                self.__print("\\x%02X"%int(char))
        else:
            self.__print("%02X "%int(char))
            
    '''
        @brief on script period
        @param[IN] seq the char sequence
        @param[IN] isdelayed if true this a delayed response
        @return True if should continue
    '''
    def onScriptPeriod(self, seq, isdelayed=False):             
        if not self.__vtmode:                      
            self.__tagtime = True
            t = "TIMED REQUEST"
            if isdelayed :
                t= "DELAYED RESPONSE"
            self.__printtime("\n\n\r"+self.INFO_COLOR+t+" : "+self.SEQ_COLOR + seq.Title()+"\n"+self.TX_COLOR+" TX")
        d = bytes(seq.Seq())
        while len(d):
            self.onTx(d[0:1])
            d = d[1:]
        return not self.__quit
        
    def printHelp(self):
        self.__term.print("\033[47;31m F1-F4 : Standard VT100 Keys | F5-F8 : Command id 1-4 | F10 : EXIT"+self.NORMAL_COLOR+"\n");

    '''
        @brief on transmit request output
        @param[IN] char the char to send
        @note to be called by Terminal
    '''
    def onTx(self, char, force=False):
        if force or ( not self.__next_cmd and not self.__skip):
            if not self.__vtmode:
                if self.__prevdir == 0:
                    self.__tagtime = True
                    self.__print("\n")
                    self.__prevdir=1
                self.__printtime("\n"+self.TX_COLOR+" TX")
                self.__printChar(char[0])
            if self.__ser:
                self.__ser.write(char)
        if not force and self.__skip : 
            self.__skip = self.__skip - 1

    '''
        @brief on byte received
        @param[IN] char the byte received
    '''            
    def __onrx(self, char):
        if self.__prevdir == 1:
            self.__tagtime = True
            self.__print("\n")
            self.__prevdir=0
        self.__printtime("\n"+self.RX_COLOR+" RX")
        self.__printChar(char)
        if self.__script:
            dd, ddt, tt=self.__script.Compute(char)
            if tt:
                if not self.__vtmode:                  
                    self.__print("\n"+self.INFO_COLOR+"FOUND : "+self.SEQ_COLOR+ tt)
            if dd:
                if not self.__vtmode:                  
                    self.__print("\n"+self.INFO_COLOR+"AUTO RESPONSE : "+self.SEQ_COLOR+ tt)
                d = bytes(dd)
                while len(d):
                    self.onTx(d[0:1], True)
                    d = d[1:]
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pyT1000 : complete serial terminal')
    parser.add_argument("-ascii", default=False, action="store_true")
    parser.add_argument("-vt100", default=False, action="store_true")
    parser.add_argument("-list", default=False, action="store_true")
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
        script = Script()
        script.load(args.s)

    t1000 = pyT1000(args.L, script)
    
    term = StdTerm(t1000.onTx)
    t1000.setTerminal(term)
    t1000.open(s)

    if args.vt100:
        t1000.setVtMode()
    elif args.ascii:
        t1000.setAsciiMode()       
    
    t1000.printHelp()
        
    t1000.join()