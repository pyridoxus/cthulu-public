'''
Created on Feb 13, 2013

@author: cmcculloch
'''
import wx

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()
EVT_STOP_ID = wx.NewId()
EVT_TIMER_ID = wx.NewId()
EVT_PROGRESS_ID = wx.NewId()

 
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

 
def EVT_TIMER(win, func):
    '''
    Define a Timer Event.
    '''
    win.Connect(-1, -1, EVT_TIMER_ID, func)

 
def EVT_PROGRESS(win, func):
    '''
    Define a Progress Event.
    '''
    win.Connect(-1, -1, EVT_PROGRESS_ID, func)

 
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
 


class TimerEvent(wx.PyEvent):
    '''
    Simple event to tell the GUI to update the timer during the running test.
    '''
    def __init__(self, data):
        '''
        Init Timer Event.
        '''
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_TIMER_ID)
        self.data = data    # The text containing the elapsed time
 


class ProgressEvent(wx.PyEvent):
    '''
    Simple event to tell the GUI to increment the progress bar.
    The data parameter isn't used at the moment because we are incrementing
    the progress bar by one.
    '''
    def __init__(self, data):
        '''
        Init Progress Event.
        '''
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_PROGRESS_ID)
        self.data = data
 


