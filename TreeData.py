'''
Created on Feb 13, 2013

@author: cmcculloch
'''
import wx

class TreeData(wx.TreeItemData):
    '''
    Retain breakpoint state, skip state, test code, etc inside the tree item.
    '''
    def __init__(self, name, parametersCode = "", moduleCode = "",
                 validatorCode = "", limitsCode = "",
                 breakPoint = False, skip = False):
        '''
        Initialize the object.
        '''
        wx.TreeItemData.__init__(self)
        self.__parametersCode = parametersCode
        self.__moduleCode = moduleCode
        self.__validatorCode = validatorCode
        self.__limitsCode = limitsCode
        self.__breakPoint = breakPoint
        self.__skip = skip
        self.__comboBreakIdx = None
        self.__comboSkipIdx = None
        self.__testName = name
        
        
    def getParametersCode(self):
        '''
        Return the parameter code string
        '''
        return self.__parametersCode


    def getModuleCode(self):
        '''
        Return the test code string
        '''
        return self.__moduleCode


    def getValidatorCode(self):
        '''
        Return the validator code string
        '''
        return self.__validatorCode


    def getLimitsCode(self):
        '''
        Return the limits code string
        '''
        return self.__limitsCode


    def getBreakPoint(self):
        '''
        Return the breakPoint state
        '''
        return self.__breakPoint


    def getSkip(self):
        '''
        Return the skip state
        '''
        return self.__skip
    

    def getComboBreakIdx(self):
        '''
        Return the index of this object in the break point combo box.
        If not in combo box, then index is None 
        '''
        return self.__comboBreakIdx


    def getComboSkipIdx(self):
        '''
        Return the index of this object in the skipped tests combo box.
        If not in combo box, then index is None 
        '''
        return self.__comboSkipIdx
    

    def getName(self):
        '''
        Get name of the test module. This is created as the test is being
        assembled from the database and into the tree. 
        '''
        return self.__testName
    

    def setParametersCode(self, parametersCode):
        '''
        Set the parameter code string
        '''
        self.__parametersCode = parametersCode
        

    def setModuleCode(self, moduleCode):
        '''
        Set the test code string
        '''
        self.__moduleCode = moduleCode
        

    def setValidatorCode(self, validatorCode):
        '''
        Set the validator code string
        '''
        self.__validatorCode = validatorCode
        

    def setLimitsCode(self, limitsCode):
        '''
        Set the limits code string
        '''
        self.__limitsCode = limitsCode
        

    def setBreakPoint(self, breakPoint):
        '''
        Set the breakPoint state
        '''
        self.__breakPoint = breakPoint
        

    def setSkip(self, skip):
        '''
        Set the skip state
        '''
        self.__skip = skip
    

    def setComboBreakIdx(self, idx):
        '''
        Set the index of this object in the break point combo box.
        If not in combo box, then index is None 
        '''
        self.__comboBreakIdx = idx


    def setComboSkipIdx(self, idx):
        '''
        Set the index of this object in the skipped tests combo box.
        If not in combo box, then index is None 
        '''
        self.__comboSkipIdx = idx


    def setName(self, name):
        '''
        Set name of the test module. This is created as the test is being
        assembled from the database and into the tree. 
        '''
        self.__testName = name
    


