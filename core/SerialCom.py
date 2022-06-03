from serial import *
import serial.tools.list_ports

class SerialCom():

    def __init__(self, name="", baudrate=115200, parity=PARITY_NONE, stopbits=STOPBITS_ONE):
        self.baudrate=baudrate
        self.parity=parity
        self.stopbits=stopbits
        self.__name=name
        self.__ser = None
    
    def open(self):
        self.__ser = Serial(self.__name,
                        baudrate=self.baudrate,
                        parity=self.parity,
                        stopbits=self.stopbits, timeout=0.01)
    
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
            output.append(SerialCom(name=port.name))
            
        return output
    
    def __repr__(self):
        return "serialCom(%s){Baudrate:%d, parity:%s, stopbits:%s}"%(
                self.__name,
                self.baudrate,
                str(self.parity),
                str(self.stopbits))

   