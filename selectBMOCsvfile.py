#!/usr/bin/env python
# coding: utf8
# select a csv file to import
# spawned by BMO-Inv-new.py  with ... subprocess Popen,PIPE

class selectBMOCsvfile:

  import sys
  from java.awt import BorderLayout
  from javax.swing import BorderFactory
  from javax.swing import JFileChooser
  from javax.swing import JTextArea
  from javax.swing import JScrollPane
  from javax.swing import JButton
  from javax.swing import JToolBar
  from javax.swing import JPanel
  from javax.swing import JFrame
  from javax.swing.filechooser import FileNameExtensionFilter

#  raise Exception ("Exception")


#  frame = JFrame(runScripts.accountName)
  frame = JFrame("Pick a csv File")
  frame.setSize(200, 225)
  frame.setLayout(BorderLayout())
  panel = JPanel()

  frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)

  chooseFile = JFileChooser("/home/wayne/Downloads") # where the csv files are saved using BMO csv export tool
  filter = FileNameExtensionFilter("csv files", ["csv"])
  chooseFile.setFileFilter(filter)
  ret = chooseFile.showDialog(frame,"Import Selected File")
 
  if ret == JFileChooser.APPROVE_OPTION:
    file = chooseFile.getSelectedFile() # file is a list of strings
    desc = chooseFile.getDescription(file) # just get the file name with no path
    curdir = chooseFile.getCurrentDirectory() # says it returns a file .. just get the directory /home/wayne/Downloads
    path = file.getAbsolutePath()     # /home/wayne/Downloads/transactionHistory.csv
    canpath = file.getCanonicalPath() # /home/wayne/Downloads/transactionHistory.csv
    path2 = file.getPath()            # /home/wayne/Downloads/transactionHistory.csv
#    print chooseFile.getName(file) # just the file name
#    print file # printed the entire path plus filename ... this is a list of two strings
#    print desc # just get the file name with no path
    print "48 Processing:",path2 #
  else:
    print "50 No Selection Made"   # if I cancel or close the window .. I get this .. end up with some white space around it
    path2 = "none"
  file2 = open('/opt/moneydance/scripts/tmp/selectBMOCsvfile.txt', 'wb')
  print "53 Opened", file2
  file2.write(path2)
  file2.close()
  print "56 Done selectBMOCsvfile.py"

##  exit(0) crahes moneydance
