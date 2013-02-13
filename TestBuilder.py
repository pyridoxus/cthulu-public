'''
Created on Feb 13, 2013

@author: cmcculloch
'''
import wx
from CompiledModule import CompiledModule

class TestBuilder(object):
    '''
    Build the individual tests and insert it into the bundle.
    '''
    
    def __init__(self):
        '''
        Initialize the TestBuilder object.
        '''
        pass # nothing to do, but may need it later.
    
    
    def build(self, item, paramDict):
        '''
        Pre-compile the code and append to the code list in the bundle.
        Load the bundle with compiled test code from the treeData object.
        treeData is an instance of the data from the module in the tree.
        '''
        tree = paramDict["tree"]
        treeData = wx.TreeCtrl.GetPyData(tree, item)
        bundle = paramDict["bundle"]
        module = CompiledModule(treeData.getName())
        
        strParametersCode = treeData.getParametersCode()
        if "def parameters(" not in strParametersCode:
#TODO: Will raise an exception in future work
            return
        # Compile the code
        parametersCode = compile(strParametersCode, '<string>', 'exec')
        parametersNS = {}   # Assign the namespace dictionary
        exec parametersCode in parametersNS     # IGNORE:W0122
        parameters = parametersNS['parameters']  # Setup bundle function

        strModuleCode = treeData.getModuleCode()
        if "def module(" not in strModuleCode:
#TODO: Will raise an exception in future work
            return
        moduleCode = compile(strModuleCode, '<string>', 'exec')
        moduleNS = {}   # Assign the namespace dictionary
        exec moduleCode in moduleNS     # IGNORE:W0122
        moduleCode = moduleNS['module']  # Setup bundle function

        strValidatorCode = treeData.getValidatorCode()
        if "def validate(" not in strValidatorCode:
#TODO: Will raise an exception in future work
            return
        valitatorCode = compile(strValidatorCode, '<string>', 'exec')
        valitatorNS = {}   # Assign the namespace dictionary
        exec valitatorCode in valitatorNS     # IGNORE:W0122
        validate = valitatorNS['validate']  # Setup bundle function

        strLimitsCode = treeData.getLimitsCode()
        if "def limits(" not in strLimitsCode:
#TODO: Will raise an exception in future work
            return
        limitsCode = compile(strLimitsCode, '<string>', 'exec')
        limitsNS = {}   # Assign the namespace dictionary
        exec limitsCode in limitsNS     # IGNORE:W0122
        limits = limitsNS['limits']  # Setup bundle function
        
        module.set(parameters, moduleCode, validate, limits, bundle)
        bundle.appendCompiledModule(module)

    

