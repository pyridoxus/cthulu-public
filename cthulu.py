'''
Created on Feb 13, 2013

@author: cmcculloch
'''

import wx
from GUI import MainFrame

class CthuluApp(wx.App):
    '''
    Driver class.
    '''
    def OnInit(self):
        '''
        Do the following when initializing the app. Set up frame, etc.
        '''
        wx.InitAllImageHandlers()
        mainFrame = MainFrame(None, -1, "")
        self.SetTopWindow(mainFrame)
        mainFrame.Show()
        mainFrame.Raise()
        return 1

# end of class CthuluApp

if __name__ == "__main__":
    cthuluApp = CthuluApp(0)
    cthuluApp.MainLoop()
