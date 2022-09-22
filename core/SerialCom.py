from serial import *
import serial.tools.list_ports
from enum import Enum

'''
    @brief serial com parity
'''
class SerialCom_Parity(Enum):
    NONE=PARITY_NONE
    ODD=PARITY_ODD
    EVEN=PARITY_EVEN

'''
    @brief serial stop bits
'''
class SerialCom_Stop(Enum):
    STP1=STOPBITS_ONE
    STP1_5=STOPBITS_ONE_POINT_FIVE
    STP2=STOPBITS_TWO

class SerialCom():

    '''
        @brief initialize SerialCom
        @param[IN] name port name
        @param[IN] baudrate the baudrate
        @param[IN] parity the parity
        @param[IN] stopbits the stop bits
    '''
    def __init__(self, name="", baudrate=115200, parity=SerialCom_Parity.NONE, stopbits=SerialCom_Stop.STP1):
        self.baudrate=baudrate
        self.parity=parity
        self.stopbits=stopbits
        self.__name=name
        self.__ser = None
    
    '''
        @brief open port
    '''
    def open(self):
        self.__ser = Serial(self.__name,
                        baudrate=self.baudrate,
                        parity=self.parity.value,
                        stopbits=self.stopbits.value, timeout=0.01)
                        
    '''
        @brief close port
    '''
    def close(self):
        self.__ser.close()
        
    '''
        @brief read data
        @param[IN] count amount of data
        @return data read or None
    '''
    def read(self, count):
        if self.__ser:
            return self.__ser.read(count)
        return None
            
    '''
        @brief write data
        @param[IN] data data to send
    '''
    def write(self, data):
        if self.__ser:
            self.__ser.write(data)
            
    '''
        @brief list available port name
        @return port name list
    '''
    def list_ports():
        ports = serial.tools.list_ports.comports()
        output = []
        for port in ports:
            output.append(port.name)
            
        return output
            
    '''
        @brief string
        @return string
    '''
    def __str__(self):
        return "serialCom(%s){Baudrate:%d, parity:%s, stopbits:%s}"%(
                self.__name,
                self.baudrate,
                str(self.parity),
                str(self.stopbits))    
            
    '''
        @brief representation
        @return representation
    '''
    def __repr__(self):
        return "serialCom(%s)"%(self.__name)

   