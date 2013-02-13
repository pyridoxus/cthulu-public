'''
Created on Feb 13, 2013

@author: cmcculloch
'''
import wx
from TestThread import TestThread
import threading
from copy import copy
from CustomEvents import ResultEvent, StopEvent


class Bundle():
    '''
    A bundle object contains all the necessary information to run tests on the
    test system.
    '''
    def __init__(self, output, parent):
        '''
        Initialize the internal data.
        '''
        self.parameters = None
        self.module = None
        self.limits = None
        self.validate = None
        self.uutCom = None
        self.db = None
        self.__testData = []    # List of { "TestName" : [Test, Results] }
        self.__testCode = []    # List of pre-compiled test code
        self.testResult = None    # Temp store test results (after limit check)
        self.testResponse = None  # Temp store UUT response to test
        self.testLimits = None    # Temp hold limits object (holds units, etc)
        self.moduleData = None  # Temp store of any test data generated
        self.__testName = ""    # Full name of test
        self.__testThread = None    # Thread running the test
        self.__guiOutput = output    # Point to GUI output text control
        self.__parent = parent      # Parent window
        self.__message = ""         # Message from GUI
        self.__validMessage = False         # Flag for a valid message present
        self.__msgLock = threading.Lock()   # Message lock
        self.__validMsgLock = threading.Lock()  # Flag lock
        
        
    def haveMessage(self):
        '''
        Return True if a message is ready for the test thread from GUI.
        '''
        return self.__validMessage


    def getMessage(self):
        '''
        Return the message and reset flags.
        '''
        self.__msgLock.acquire()
        msg = copy(self.__message)  # Make a copy that is thread safe
        self.__message = ""         # Reset the message
        self.__msgLock.release()

        self.__validMsgLock.acquire()
        self.__validMessage = False
        self.__validMsgLock.release()
        return msg
    
    
    def setMessage(self, msg, wait = False):
        '''
        Set the message from GUI to test thread.
        '''
        self.__msgLock.acquire()
        self.__message = copy(msg)  # Make a copy that is thread safe
        self.__msgLock.release()
        
        self.__validMsgLock.acquire()
        self.__validMessage = True
        self.__validMsgLock.release()
        
        if wait:    # Wait until other thread got the message
            flag = False
            while not flag: # TODO: Should have a timeout here?
                self.__validMsgLock.acquire()
                if not self.__validMessage: # Other thread got message
                    flag = True
                self.__validMsgLock.release()
        
        return msg

    
    def output(self, text):
        '''
        Send the text to the GUI text control via an event handler.
        This is thread-safe.
        '''
        wx.PostEvent(self.__parent, ResultEvent("%s\n" % text))


    def stop(self, text):
        '''
        Send a signal to stop the test.
        '''
        wx.PostEvent(self.__parent, StopEvent("%s\n" % text))
        
        
        
    def packTestData(self, state = True):
        '''
        If state is True, then Store all test results, response, limits, etc.
        in testData[], otherwise do nothing.
        '''
        if state:
            self.__testData.append({ self.__testName :
                                     { "response" : self.testResponse ,
                                       "limits"   : self.testLimits,
                                       "result"   : self.testResult }
                                   })
            
            
    def load(self, parameters, module, validate, limits):
        ''' Load the bundle with the test functions '''
        self.parameters = parameters
        self.module = module
        self.validate = validate
        self.limits = limits
        
        
    def start(self):
        '''
        Start the module test code.
        '''
        if self.__testThread is None:
            self.__testThread = TestThread(self.__testCode, self)
            self.__testThread.start()
        else:
            raise RuntimeError("Test thread was not deleted properly")
        
        
        
    def setUUTCom(self, uutCom):
        ''' Initialize the uutCom object '''
        self.uutCom = uutCom
        
        
    def setDB(self, db):
        ''' Initialize the database object '''
        self.db = db
        
        
    def setTestName(self, name):
        '''
        Set the name of the test. This name will be used to store all the
        test data and test results from the test.
        '''
        self.__testName = name
        
        
    def appendCompiledModule(self, module):
        '''
        Append the compiled module to the list to be run later.
        '''
        self.__testCode.append(module)
        


