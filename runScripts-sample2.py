#!/usr/bin/env jython
# coding: utf8
# this is a Java Swing program
# the print statements show up on the Jython Console, you can run it with
#>>> exexfile("runScripts.py")
# the moneydance Console will also show any major errors


BMOAccounts = ['Account1',
               'Account2',
               'Account3',
	       'Account4',
	       'Account5',
	       'Account6']


class runScripts:  

  import sys
  #from javax.swing import *
  #from java.awt import *
  from javax.swing.tree import DefaultMutableTreeNode
###  from com.moneydance.apps.md.model import AbstractTxn
###  from com.moneydance.apps.md.model import ParentTxn
###  from com.moneydance.apps.md.model import SplitTxn
  from com.infinitekind.moneydance.model import AbstractTxn
  from com.infinitekind.moneydance.model import ParentTxn
  from com.infinitekind.moneydance.model import SplitTxn

  from javax.swing import Timer
  from java.awt.event import ActionListener
  from javax.swing import JFrame
  from java.awt import BorderLayout
  from javax.swing import JTree
  from javax.swing import JScrollPane
  from java.awt import Dimension
  from javax.swing import JPanel
  from javax.swing import JButton
  from javax.swing import JLabel
  from javax.swing import WindowConstants

  import os
  os.chdir('/opt/moneydance/scripts')
      
  class WindowClose(ActionListener):
    def __init__(self):
        from javax.swing import Timer
        self.timer = Timer(5000, self)
        self.timer.start()
    def actionPerformed(self, e):
        self.timer.stop()
        mframe.dispose()  

  
  def showMessage (self,message) : 
    global mframe
    mframe = self.JFrame("Message")
#    mframe = self.JFrame(message)
#    mframe.setSize(1000, 100)
    mframe.setSize(1000, 50)
    mframe.setDefaultCloseOperation(self.WindowConstants.DISPOSE_ON_CLOSE)
    mpnl = self.JPanel()
    mframe.add(mpnl)
    mlabel = self.JLabel(str(message))
    mpnl.add(mlabel)
    mlabel.setVisible(True)
    mframe.setVisible(True)
    self.WindowClose()


  def addLevel2Items(self,branch, branchData=None):
    '''  add data to tree branch
         requires branch and data to add to branch
    '''
    # this does not check to see if its a valid branch
    if branchData == None:
        branch.add(DefaultMutableTreeNode('No valid data'))
    else:
        for item in branchData:
          # add the data from the specified list to the branch
          branch.add(self.DefaultMutableTreeNode(item))

  def ItemSelect(self, event):
    import sys
    selected = self.tree.getLastSelectedPathComponent()
    if selected == None:
      xlabel.text = 'No script selected'
    else:
      self.xlabel.text = str(selected)
      print "Selected ", selected

      if str(selected).count("Misc Scripts"):
          mess = "Error Please Select a Misc Script From the list below"
          self.showMessage(mess)   
      elif str(selected).count("Run Stockwatch Update Scripts"): 
          mess = "Error Please Select a Stockwatch Update Script From the list below"
          self.showMessage(mess)
      elif str(selected).count("Import BMO transaction"):
          mess = "Error Please Select an Investment Account From the list below"
          self.showMessage(mess)
      elif str(selected).count('/opt/moneydance/scripts/updateHistoryStockwatch.py'): 
          mess = 'updateHistoryStockwatch.py Can Take a Long Time to Finish 6 minutes per Symbol'
          self.showMessage(mess)        
	  execfile(str(selected))  	  	      
      elif str(selected) in BMOAccounts:
          mess = "Updating BMOAccount "+ str(selected)
          self.showMessage(mess)
          sys.argv = ['','runScripts',str(selected)]
	  execfile("/opt/moneydance/scripts/BMO-Inv-new.py")
      else:
          mess = "Running Script "+ str(selected)
          self.showMessage(mess)
          execfile(str(selected))
          
  def __init__(self):
      
    import sys
    from javax.swing import JEditorPane
    from javax.swing import JFrame
    from javax.swing import JPanel
    from javax.swing import JScrollPane
    from javax.swing import JSplitPane

    from java.awt import Color
    from javax.swing import ImageIcon
    from javax.swing.tree import DefaultTreeCellRenderer
    from javax.swing import JTree
    from javax.swing.tree import DefaultMutableTreeNode
    from javax.swing.tree import TreeSelectionModel
    from javax.swing.event import TreeSelectionEvent
    from javax.swing.event import TreeSelectionListener
    from javax.swing.plaf.metal import MetalIconFactory

 
# the list of Misc Scripts test.py and dev.py are just for playing with
    mMiscData = ["StockGlance75.py","jython_info.py" ,"test.py","dev.py"]
# the scripts below process csv files downloaded from www.stockwatch.com and manually placed in
# /opt/moneydance/tmp/Stockwatch (maybe a years history in each file , a separate file for each symbol)
#  StockwatchDay(fetches the days closing prices for that exchange and updates Moneydance automatically)
    sStockwatchData = ["updateDaylyStockwatch.py" ,"updateHistoryStockwatch.py"]

    upBMOInvestmentPyData = BMOAccounts

    xframe = self.JFrame("runScripts.py")
#    xframe.setSize(500, 350)
    xframe.setSize(800, 350)
    xframe.setLayout(self.BorderLayout())

    # add level 0 items
    treeRoot = self.DefaultMutableTreeNode('Jython Scripts')
    
    mMisc = self.DefaultMutableTreeNode('Misc Scripts')
    sStockwatch = self.DefaultMutableTreeNode('Run Stockwatch Update Scripts')
    upBMOInvestmentPy = self.DefaultMutableTreeNode('Import BMO transaction from ~/Downloads/*.csv to the selected Investment Account')
    
    # add the level 1 items
    treeRoot.add(mMisc)
    treeRoot.add(sStockwatch)
    treeRoot.add(upBMOInvestmentPy)

    #add the level 2 items to level 1
    self.addLevel2Items(mMisc, mMiscData)
    self.addLevel2Items(sStockwatch, sStockwatchData)
    self.addLevel2Items(upBMOInvestmentPy, upBMOInvestmentPyData)
    
    #build the tree
    self.tree = self.JTree(treeRoot)

    leafIcon = MetalIconFactory.getTreeLeafIcon()    
    openIcon = MetalIconFactory.getFileChooserNewFolderIcon()
    closedIcon = MetalIconFactory.getTreeFolderIcon()

    renderer = DefaultTreeCellRenderer()
    renderer.setLeafIcon(leafIcon)
    renderer.setOpenIcon(openIcon)
    renderer.setClosedIcon(closedIcon)
    self.tree.setCellRenderer(renderer)
   
        
    scrollPane = self.JScrollPane()  # add a scrollbar to the viewport
    scrollPane.setPreferredSize(self.Dimension(700,250))
    scrollPane.getViewport().setView(self.tree)

    xpanel = self.JPanel()
    xpanel.add(scrollPane)
    xframe.add(xpanel, self.BorderLayout.CENTER)

    btn = self.JButton('Run Script', actionPerformed = self.ItemSelect)
    xframe.add(btn,self.BorderLayout.SOUTH)
    self.xlabel = self.JLabel('Select Script')
    xframe.add(self.xlabel, self.BorderLayout.NORTH)
    xframe.setDefaultCloseOperation(self.WindowConstants.DISPOSE_ON_CLOSE)
    xframe.setVisible(True)
    #print "stdout1",sys.stdout
    self.addLevel2Items # initalize the addLevel2Items function
    #print "stdout2",sys.stdout

if __name__ == '__main__':
  runScripts()
  
