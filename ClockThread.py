'''
Created on Feb 14, 2013

@author: cmcculloch
'''
import threading
import time
import wx
import socket
import fcntl
import struct
from CustomEvents import ClockEvent, NetworkNotifyEvent

class ClockThread(threading.Thread):
    '''
    Simple threading class to update the clock in the GUI with both
    date and time.
    Clock thread also acts as a watchdog to check on the network connection
    and database access.
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

                
    def __getIPAddr(self, ifname):
        '''
        Get the IP Address to confirm that we are still connected to the
        network.
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
        
    
    def __postNetworkEvent(self):
        '''
        Post the Network notification icon event.
        '''
        try:
            ip = self.__getIPAddr("eth0")
            # The exception is thrown before the next line
            wx.PostEvent(self.__parent, NetworkNotifyEvent(ip))
        except IOError:
            wx.PostEvent(self.__parent, NetworkNotifyEvent(False))
        
        
    def run(self):
        '''
        Start the thread here.
        '''
        self.__update()
        while True:
            self.__startTime = time.time()
            while time.time() - self.__startTime < 60:
                if int(time.time() - self.__startTime) % 10 == 0:
                    self.__postNetworkEvent()
                if self.__kill:
                    break
                time.sleep(1)   # We don't need to loop constantly
            if self.__kill:
                break
            self.__update()
