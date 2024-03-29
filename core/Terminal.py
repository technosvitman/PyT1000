import threading
import time

class Terminal(threading.Thread):
    '''
        @brief initialize Terminal
        @param[IN] on_char on char to transmit callback
    '''
    def __init__(self, on_char):
        threading.Thread.__init__(self)
        self.__on_char = on_char
        self.__quit = False
        self.start()        
    
    '''
        @brief terminal task
    '''
    def run(self):
        output = ""
        while self.__quit==False:
            output = self.getch()
            if output and output != b''and output != b'\0':
                self.__on_char(output)   
            time.sleep(0.05)
    
    '''
        @brief get char
        @return char
    '''
    def getch(self):
        return b"\x03"  
    
    '''
        @brief close terminal
    '''
    def close(self):
        self.__quit=True
    
    '''
        @brief print char to terminal
        @param[IN] str char or string to print
    '''   
    def print(self, str):
        pass