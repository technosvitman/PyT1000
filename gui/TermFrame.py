import wx
import wx.py.editwindow as shell

class TermFrame(shell.EditWindow):

    def __init__(self, parent):
        shell.EditWindow.__init__(self, parent=parent)
        
    def print(self, text):
        self.AppendText(text)