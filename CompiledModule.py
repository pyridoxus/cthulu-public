'''
Created on Feb 13, 2013

@author: cmcculloch
'''

class CompiledModule():
    '''
    Object to contain the compiled code and other information.
    '''
    def __init__(self, testName):
        '''
        Setup the object.
        '''
        self.__parameters = None    # Will point to parameter function
        self.__module = None        # Will point to module function
        self.__validate = None      # Will point to validator function
        self.__limits = None        # Will point to limits function
        self.__bundle = None        # Will point to the bundle
        self.__testName = testName  # The name of the test
        
        
    def setBundle(self, bundle):
        '''
        Set the bundle.
        '''
        self.__bundle = bundle
        
        
    def set(self, parameters, module, validate, limits, bundle):
        '''
        Set all of the internal compiled code variables and bundle.
        '''
        self.__parameters = parameters
        self.__module = module
        self.__validate = validate
        self.__limits = limits
        self.__bundle = bundle
#        print "Setting", self.__testName, parameters, module, validate, limits, bundle
        
        
    def getTestName(self):
        '''
        Return the test name.
        '''
        return self.__testName
    
    
    def run(self):
        '''
        Run the module code.
        '''
        if self.__bundle is not None:
            # Store the current function pointers in the bundle so that
            # the module functions can access each other.
            self.__bundle.parameters = self.__parameters
            self.__bundle.module = self.__module
            self.__bundle.validate = self.__validate
            self.__bundle.limits = self.__limits
            
            # Start the module code, sending in the bundle.
            if self.__module is not None:
                self.__module(self.__bundle)
                self.__bundle.packTestData()
        

        
