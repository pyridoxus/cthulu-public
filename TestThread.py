'''
Created on Feb 13, 2013

@author: cmcculloch
'''

import threading

class TestThread(threading.Thread):
    '''
    The thread object that runs the test.
    '''
    def __init__(self, code, bundle):
        '''
        Initialize the internal data.
        '''
        threading.Thread.__init__(self, name = "testthread")
        self.__code = code          # List containing compiled code
        self.__bundle = bundle        # Bundle of test information


    def __pause(self):
        ''' Pause and wait for a message to start or stop the test.'''
        while True:
            if self.__bundle.haveMessage():
                msg = self.__bundle.getMessage()
                if msg == "STOP":
                    returnMsg = "STOP"
                    break
                if msg == "RUN":
                    returnMsg = "RUN"
                    break
                # No other messages should be sent... but we may need to 
                # process something else, which is why it's designed this way.
        return returnMsg
                
        
    def run(self):
        '''
        Start running the stored test modules.
        '''
        returnMsg = "Test finished normally"
        for module in self.__code:
            module.run()
            if self.__bundle.haveMessage():
                msg = self.__bundle.getMessage()
                if msg == "STOP":
                    returnMsg = "User stopped the test."
                    break
                if msg == "PAUSE":
                    if self.__pause() == "STOP":    # User stopped test
                        returnMsg = "User stopped the test."
                        break
            self.__bundle.incrementProgress()
                        
                
        self.__bundle.stop(returnMsg)
    
    
        
