'''
Created on Feb 14, 2013

@author: cmcculloch
'''
import threading
import time
import wx
from CustomEvents import TimerEvent
from copy import copy

class TimerThread(threading.Thread):
    '''
    The thread object that sends events to GUI to update the timer.
    '''
    def __init__(self, parent):
        '''
        Setup the internals.
        '''
        threading.Thread.__init__(self, name = "timerthread")
        self.__parent = parent
        self.__startTime = 0.0
        self.__currentTime = 0.0
        self.__msg = ""
        self.__msgLock = threading.Lock()


    def setMessage(self, msg):
        '''
        Set the message for this object in other thread.
        '''
        self.__msgLock.acquire()
        self.__msg = copy(msg)
        self.__msgLock.release()
        
        
    def getMessage(self):
        '''
        Get the message from the GUI thread.
        '''
        self.__msgLock.acquire()
        message = copy(self.__msg)
        self.__msgLock.release()
        flag = False
        if message == "STOP":
            flag = True
        return flag
            
            
    def __str__(self):
        ''' Create the elaped time string. '''
        minutes = int(self.__currentTime / 60.0)
        seconds = self.__currentTime % 60
        return "%d:%02d" % (minutes, seconds)
        
        
    def run(self):
        '''
        Start the thread by noting the current time and then updating the GUI
        once per second with the new elapsed time.
        '''
        self.__startTime = time.time()
        while True:
            if int(time.time() - self.__startTime) > self.__currentTime:
                self.__currentTime = time.time() - self.__startTime
                wx.PostEvent(self.__parent, TimerEvent("%s" % self))
            if self.getMessage():   # Thread to be killed
                break
            
        