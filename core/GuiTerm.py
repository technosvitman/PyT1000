import msvcrt
import os

from . import Terminal

class GuiTerm(Terminal):
    def __init__(self, on_char, guiframe):
        self.__gui = guiframe
        Terminal.__init__(self, on_char)
        self.print("\033[m\033[2J\033[H")
    
    def getch(self):
        return self.__gui.getch()
        
    def print(self, str):
        self.__gui.print(str)