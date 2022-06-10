from serial import *
import serial.tools.list_ports
from enum import Enum

class SerialCom_Parity(Enum):
    NONE=PARITY_NONE
    ODD=PARITY_ODD
    EVEN=PARITY_EVEN

class SerialCom_Stop(Enum):
    STP1=STOPBITS_ONE
    STP1_5=STOPBITS_ONE_POINT_FIVE
    STP2=STOPBITS_TWO

class SerialCom():

    def __init__(self, name="", baudrate=115200, parity=SerialCom_Parity.NONE, stopbits=SerialCom_Stop.STP1):
        self.baudrate=baudrate
        self.parity=parity
        self.stopbits=stopbits
        self.__name=name
        self.__ser = None
    
    def open(self):
        self.__ser = Serial(self.__name,
                        baudrate=self.baudrate,
                        parity=self.parity.value,
                        stopbits=self.stopbits.value, timeout=0.01)
    
    def close(self):
        self.__ser.close()
    
    def read(self, count):
        if self.__ser:
            return self.__ser.read(count)
        return None
    
    def write(self, data):
        if self.__ser:
            self.__ser.write(data)
    
    def list_ports():
        ports = serial.tools.list_ports.comports()
        output = []
        for port in ports:
            output.append(port.name)
            
        return output
    
    def __str__(self):
        return "serialCom(%s){Baudrate:%d, parity:%s, stopbits:%s}"%(
                self.__name,
                self.baudrate,
                str(self.parity),
                str(self.stopbits))
    
    def __repr__(self):
        return "serialCom(%s)"%(self.__name)

   