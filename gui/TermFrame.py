import wx
import wx.stc as shell

class TermFrame(shell.StyledTextCtrl):

    def __init__(self, parent):
        shell.StyledTextCtrl.__init__(self, parent=parent)        
        self.__in = []
        self.Bind(wx.EVT_KEY_DOWN, self.DoKeyPress)
        
    def print(self, text):
        self.write(text)
        
    def DoKeyPress(self, event):
        keycode = event.GetKeyCode()
        self.__in.append(bytes(keycode))
        
    def getch(self):
        if len(self.__in) :
            return self.__in.pop(0)
        else:
            return None