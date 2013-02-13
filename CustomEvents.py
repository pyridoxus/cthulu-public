'''
Created on Feb 13, 2013

@author: cmcculloch
'''
import wx

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()
EVT_STOP_ID = wx.NewId()

 
def EVT_RESULT(win, func):
    '''
    Define Result Event.
    '''
    win.Connect(-1, -1, EVT_RESULT_ID, func)
    
    
def EVT_STOP(win, func):
    '''
    Define a Stop Test Event.
    '''
    win.Connect(-1, -1, EVT_STOP_ID, func)

 
class ResultEvent(wx.PyEvent):
    '''
    Simple event to carry arbitrary result data.
    '''
    def __init__(self, data):
        '''
        Init Result Event.
        '''
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
 


class StopEvent(wx.PyEvent):
    '''
    Simple event to tell the GUI that the test has stopped due to error or
    normal completion.
    '''
    def __init__(self, data):
        '''
        Init Stop Event.
        '''
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_STOP_ID)
        self.data = data    # Some kind of message about the stopping of test
 


