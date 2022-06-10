import threading

class Terminal(threading.Thread):
    def __init__(self, on_char):
        threading.Thread.__init__(self)
        self.__on_char = on_char
        self.start()        
    
    def run(self):
        output = ""
        while output != b"\x03":
            output = self.getch()
            self.__on_char(output)        
        self.print("\033[m\033[2J\033[H")
    
    def getch(self):
        return b"\x03"
                
        
    def print(self, str):
        pass