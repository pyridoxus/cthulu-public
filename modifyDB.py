#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Tue Feb 26 09:46:02 2013

'''
Created on Feb 25, 2013

@author: cmcculloch
'''

import wx
import psycopg2
import string

class Database():
    '''
    Database connection class.
    '''
    def __init__(self, ip = "127.0.0.1"):
        '''
        Setup internals.
        '''
        self.__ip = ip
        self.__conn = None
        self.__cur = None
        self.__DBreturning = None
        
        
    def insert(self, table, insertDict, returningList):
        '''
        Insert the values of the dictionary where the keys are the column
        names into the table. Use returningList to indicate which columns
        to be returned from the insertion.
        '''

        columnString = ""
        valueString = ""
        i = iter(insertDict)
        while True:
            try:
                column = i.next()
                columnString += "%s," % column
                valueString += "%s," % insertDict[column]
            except StopIteration:
                columnString = columnString[0:-1]   # Remove training comma
                valueString = valueString[0:-1]   # Remove training comma
                break
            
        returningString = ""
        if len(returningList) > 0:
            returningString = "RETURNING ("
            for item in returningList:
                returningString += "%s," % item
            returningString = returningString[0:-1] # Remove training comma
            returningString += ")"  # closing parentheses
        
        s = "INSERT INTO %s (%s) VALUES (%s) %s;" % (table,
                                                    columnString,
                                                    valueString,
                                                    returningString)
                            
        print s
        try:
            self.__conn = psycopg2.connect("dbname='cthulu' "
                                           "user='postgres' "
                                           "host='%s' "
                                           "password='wibble'"
                                           % self.__ip)
        except:
#TODO: Need to throw an exception, store in log file, etc
            print "I am unable to connect to the database"
        
        self.__cur = self.__conn.cursor()
        self.__cur.execute(s)
        self.__conn.commit()
        
        # Returning a tuple containing uuid and execTime
        DBReturning = self.__cur.fetchone()[0]
        self.__cur.close()
        self.__conn.close()
        return DBReturning


    def __splitDBReturning(self):
        '''
        Split the returning string from the DB and return two strings.
        '''
        uuid, date = string.split(self.__DBreturning, ",")
        uuid = uuid[1:] # Drop the opening parenthesis
        date = date[1:-2]   # Drop the ending parenthesis and both quotes
        print uuid, date
        return uuid, date
        
    

class SuiteFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: SuiteFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.sizerSuites_staticbox = wx.StaticBox(self, -1, "Test Suites")
        self.treeCode = wx.TreeCtrl(self, -1,
                                    style=wx.TR_HAS_BUTTONS| \
                                    wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)
        self.textInfo = wx.TextCtrl(self, -1, "Script Information",
                                    style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.textCode = wx.TextCtrl(self, -1, "",
                                    style=wx.TE_MULTILINE)
        
        # Menu Bar
        self.mainFrameMenu = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.NewId(), "&Reload",
                                "Reload the tree of code", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.NewId(), "Re&vert",
                                "Discard changes and revert "\
                                "to last known state", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.NewId(), "E&xit", "", wx.ITEM_NORMAL)
        self.mainFrameMenu.Append(wxglade_tmp_menu, "&File")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.NewId(), "&Connect", "", wx.ITEM_NORMAL)
        self.mainFrameMenu.Append(wxglade_tmp_menu, "&Database")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu_sub = wx.Menu()
        wxglade_tmp_menu_sub.Append(wx.NewId(), "Scrip&t", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.Append(wx.NewId(), "&Module", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.Append(wx.NewId(), "&Block", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.Append(wx.NewId(), "&Suite", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendMenu(wx.NewId(), "&Increment version",
                                    wxglade_tmp_menu_sub, "")
        wxglade_tmp_menu_sub = wx.Menu()
        wxglade_tmp_menu_sub.Append(wx.NewId(), "Scrip&t", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.Append(wx.NewId(), "&Module", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.Append(wx.NewId(), "&Block", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.Append(wx.NewId(), "&Suite", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendMenu(wx.NewId(), "&Branch version",
                                    wxglade_tmp_menu_sub, "")
        self.mainFrameMenu.Append(wxglade_tmp_menu, "&Commit")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.NewId(), "&Help", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.NewId(), "&About", "", wx.ITEM_NORMAL)
        self.mainFrameMenu.Append(wxglade_tmp_menu, "&Help")
        self.SetMenuBar(self.mainFrameMenu)
        # Menu Bar end

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.onFileReload, id=-1)
        self.Bind(wx.EVT_MENU, self.onFileRevert, id=-1)
        self.Bind(wx.EVT_MENU, self.onFileExit, id=-1)
        self.Bind(wx.EVT_MENU, self.onDatabaseConnect, id=-1)
        self.Bind(wx.EVT_MENU, self.onMenuCommitIncrementScript, id=-1)
        self.Bind(wx.EVT_MENU, self.onMenuCommitIncrementModule, id=-1)
        self.Bind(wx.EVT_MENU, self.onMenuCommitIncrementBlock, id=-1)
        self.Bind(wx.EVT_MENU, self.onMenuCommitIncrementSuite, id=-1)
        self.Bind(wx.EVT_MENU, self.onMenuCommitBranchScript, id=-1)
        self.Bind(wx.EVT_MENU, self.onMenuCommitBranchModule, id=-1)
        self.Bind(wx.EVT_MENU, self.onMenuCommitBranchBlock, id=-1)
        self.Bind(wx.EVT_MENU, self.onMenuCommitBranchSuite, id=-1)
        self.Bind(wx.EVT_MENU, self.onMenuHelpHelp, id=-1)
        self.Bind(wx.EVT_MENU, self.onMenuHelpAbout, id=-1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: SuiteFrame.__set_properties
        self.SetTitle("Cthulu Database Interface")
        self.SetSize((1200, 1023))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: SuiteFrame.__do_layout
        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMainVertical = wx.BoxSizer(wx.VERTICAL)
        sizerMainCode = wx.BoxSizer(wx.HORIZONTAL)
        sizerSelector = wx.BoxSizer(wx.HORIZONTAL)
        sizerSuites = wx.StaticBoxSizer(self.sizerSuites_staticbox, wx.VERTICAL)
        sizerSuites.Add(self.treeCode, 1, wx.EXPAND, 0)
        sizerSelector.Add(sizerSuites, 1, wx.EXPAND, 0)
        sizerMainVertical.Add(sizerSelector, 1, wx.EXPAND, 0)
        sizerMainCode.Add(self.textInfo, 1, wx.EXPAND, 0)
        sizerMainCode.Add(self.textCode, 4, wx.EXPAND, 0)
        sizerMainVertical.Add(sizerMainCode, 3, wx.EXPAND, 0)
        sizerMain.Add(sizerMainVertical, 1, wx.EXPAND, 0)
        self.SetSizer(sizerMain)
        self.Layout()
        # end wxGlade

    # wxGlade: SuiteFrame.<event_handler>
    def onFileReload(self, event):
        print "Event handler `onFileReload' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onFileRevert(self, event):
        print "Event handler `onFileRevert' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onFileExit(self, event):
        print "Event handler `onFileExit' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onDatabaseConnect(self, event):
        print "Event handler `onDatabaseConnect' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onMenuCommitIncrementScript(self, event):
        print "Event handler `onMenuCommitIncrementScript' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onMenuCommitIncrementModule(self, event):
        print "Event handler `onMenuCommitIncrementModule' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onMenuCommitIncrementBlock(self, event):
        print "Event handler `onMenuCommitIncrementBlock' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onMenuCommitIncrementSuite(self, event):
        print "Event handler `onMenuCommitIncrementSuite' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onMenuCommitBranchScript(self, event):
        print "Event handler `onMenuCommitBranchScript' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onMenuCommitBranchModule(self, event):
        print "Event handler `onMenuCommitBranchModule' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onMenuCommitBranchBlock(self, event):
        print "Event handler `onMenuCommitBranchBlock' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onMenuCommitBranchSuite(self, event):
        print "Event handler `onMenuCommitBranchSuite' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onMenuHelpHelp(self, event):
        print "Event handler `onMenuHelpHelp' not implemented!"
        event.Skip()

    # wxGlade: SuiteFrame.<event_handler>
    def onMenuHelpAbout(self, event):
        print "Event handler `onMenuHelpAbout' not implemented!"
        db = Database()
        print db.insert("scripts", { "script_key" : "DEFAULT",
                                     "object_data_key" : 1,
                                     "script" : "'print \"Hello World!\"'",
                                     "script_steps" : 1 }, ["script_key"])
        event.Skip()

# end of class SuiteFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    mainFrame = SuiteFrame(None, -1, "")
    app.SetTopWindow(mainFrame)
    mainFrame.Show()
    app.MainLoop()
