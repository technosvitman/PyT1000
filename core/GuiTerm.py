import msvcrt
import os

from . import Terminal

class GuiTerm(Terminal):
    def __init__(self, on_char, guiframe):
        Terminal.__init__(self, on_char)
        self.__gui = guiframe
        self.print("\033[m\033[2J\033[H")
    
    def getch(self):
        return None
        
    def print(self, str):
        self.__gui.print(str)