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
EVT_CLOCK_ID = wx.NewId()
EVT_DATABASE_NOTIFY_ID = wx.NewId()
EVT_NETWORK_NOTIFY_ID = wx.NewId()

 
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

 
def EVT_CLOCK(win, func):
    '''
    Define a Clock Event.
    '''
    win.Connect(-1, -1, EVT_CLOCK_ID, func)

 
def EVT_DATABASE_NOTIFY(win, func):
    '''
    Define a Database Notify Event.
    '''
    win.Connect(-1, -1, EVT_DATABASE_NOTIFY_ID, func)

 
def EVT_NETWORK_NOTIFY(win, func):
    '''
    Define a Network Notify Event.
    '''
    win.Connect(-1, -1, EVT_NETWORK_NOTIFY_ID, func)

 
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
 


class ClockEvent(wx.PyEvent):
    '''
    Simple event to tell the GUI to update the clock for both date and time.
    The data parameter isn't used.
    '''
    def __init__(self, dateText, timeText):
        '''
        Init Clock Event.
        '''
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_CLOCK_ID)
        self.data = {}
        self.data["date"] = dateText
        self.data["time"] = timeText
 


class DatabseNotifyEvent(wx.PyEvent):
    '''
    Simple event to tell the GUI to update the database notification icon.
    '''
    def __init__(self, state):
        '''
        Init Database Notification Event.
        '''
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_DATABASE_NOTIFY_ID)
        self.data = state # If state is true, then the icon will show active
 


class NetworkNotifyEvent(wx.PyEvent):
    '''
    Simple event to tell the GUI to update the network notification icon.
    '''
    def __init__(self, state):
        '''
        Init Network Notification Event.
        '''
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_NETWORK_NOTIFY_ID)
        self.data = state
 


