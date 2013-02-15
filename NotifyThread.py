'''
Created on Feb 15, 2013

@author: cmcculloch
'''
import threading
from time import sleep
import wx
from copy import copy
from CustomEvents import DatabseNotifyEvent, NetworkNotifyEvent

class NotifyThread(threading.Thread):
    '''
    Simple threading class to toggle the notification icons in the GUI thread.
    '''
    def __init__(self, parent):
        '''
        Init the internals.
        '''
        threading.Thread.__init__(self, name = "notifythread")
        self.__parent = parent
        self.__kill = False
        self.__msgList = []
        self.__msgLock = threading.Lock()
        

    def kill(self):
        '''
        Set the kill flag for this thread.
        '''
        self.__kill = True      

                
    def setMsg(self, message):
        '''
        Items are appended to the message list because it's possible for this
        thread to be busy and possible miss a message.
        '''
        self.__msgLock.acquire()
        self.__msgList.append(message)
        self.__msgLock.release()
        
        
    def __getMsg(self):
        '''
        Get the message safely.
        '''
        self.__msgLock.acquire()
        if len(self.__msgList) > 0:
            message = self.__msgList.pop()
        else:
            message = ""
        self.__msgLock.release()
        return message
        
            
    def __toggleDatabaseNotify(self):
        '''
        Toggle the database icon in the notification bar.
        '''
        wx.PostEvent(self.__parent, DatabseNotifyEvent(True))
        sleep(0.5)
        wx.PostEvent(self.__parent, DatabseNotifyEvent(False))
        
        
    def __networkNotify(self, state):
        '''
        Set/reset the network icon in the notification bar.
        '''
        wx.PostEvent(self.__parent, NetworkNotifyEvent(state))
        
        
    def run(self):
        '''
        Start the thread here.
        '''
        while True:
            if self.__kill:
                break
            sleep(0.1)   # We don't need to loop constantly
            message = self.__getMsg()
            if message == "DATABASE":
                self.__toggleDatabaseNotify()
            if message == "NETWORK ON":
                self.__networkNotify(True)
            if message == "NETWORK OFF":
                self.__networkNotify(False)
            