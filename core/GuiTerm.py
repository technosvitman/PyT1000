import msvcrt
import os

from . import Terminal

class GuiTerm(Terminal):
    
    '''
        @brief init GuiTerm
        @see Terminal
        @todo in progress
    '''   
    def __init__(self, on_char, guiframe):
        self.__gui = guiframe
        Terminal.__init__(self, on_char)
        self.print("\033[m\033[2J\033[H")
    
    '''
        @brief get char
        @see Terminal
    '''   
    def getch(self):
        return self.__gui.getch()
        
    '''
        @brief print char
        @see Terminal
    '''   
    def print(self, str):
        self.__gui.print(str)