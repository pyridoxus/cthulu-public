'''
Created on Feb 14, 2013

@author: cmcculloch
'''
import threading
import time
import wx
from CustomEvents import ClockEvent

class ClockThread(threading.Thread):
    '''
    Simple threading class to update the clock in the GUI with both
    date and time.
    '''
    def __init__(self, parent):
        '''
        Init the internals.
        '''
        threading.Thread.__init__(self, name = "clockthread")
        self.__parent = parent
        self.__startTime = 0.0
        self.__currentTime = 0.0
        self.__kill = False
        

    def __update(self):
        '''
        Update GUI clock.
        '''
        text = time.asctime()
        d = text.split(" ")
        dateText = "%s %s %s" % (d[0], d[1], d[2])
        d = d[3].split(":")
        timeText = "%s:%s" % (d[0], d[1])
        wx.PostEvent(self.__parent, ClockEvent(dateText, timeText))
        
        
    def kill(self):
        '''
        Set the kill flag for this thread.
        '''
        self.__kill = True      

                
    def run(self):
        '''
        Start the thread here.
        '''
        self.__update()
        while True:
            self.__startTime = time.time()
            while time.time() - self.__startTime < 60:
                if self.__kill:
                    break
                time.sleep(1)   # We don't need to loop constantly
            if self.__kill:
                break
            self.__update()
