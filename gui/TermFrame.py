import wx
import wx.py.shell as shell

class TermFrame(shell.Shell ):

    def __init__(self, parent):
        shell.Shell.__init__(self, parent=parent)        
        self.__in = []
        self.Bind(wx.EVT_KEY_DOWN, self.DoKeyPress)
        self.clear()
        
    def print(self, text):
        self.write(text)
        
    def DoKeyPress(self, event):
        keycode = event.GetKeyCode()
        self.__in.append(bytes(keycode))
        event.Skip()
        
    def getch(self):
        if len(self.__in) :
            return self.__in.pop(0)
        else:
            return None