import msvcrt
import os

from . import Terminal

class StdTerm(Terminal):
    def __init__(self, on_char):
        Terminal.__init__(self, on_char)
        os.system("")
        self.print("\033[m\033[2J\033[H")
    
    def getch(self):
        return msvcrt.getch() 
        
    def print(self, str):
        print(str, end='', flush=True)