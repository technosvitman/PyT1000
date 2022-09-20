import wx

from .TermFrame import TermFrame

class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='pyT1000')
        
        self.__term = TermFrame(self)

    def GetTerm(self):
        return self.__term
        
        