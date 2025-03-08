#!/usr/bin/env python
# coding: utf8
# version 2/21/2025

# this script is started by the Bash script qfxStripper
# its stdout and stderr are redirected to /opt/moneydance/scripts/qfxStripper.log
# so look there for messgaes
# it makes no changes to Scotia , Canadian Tire and CIBC qfx files but will change all the EDT timezones in BMO files to MST
# will most likely work on any qfx with EDT
# associate the gsxStripper bash script with the *.qfx file extension in KDE
# then all you have to do is click on the qfx file displayed in Dolphin an a new file will appear with the word fixed in its name
# just drag and drop the *fixed* file into moneydance.

import sys

#sys.stdout = open ('/opt/moneydance/scripts/qfx.log', 'w')
#sys.stderr = open ('/opt/moneydance/scripts/qfx.log', 'w')
#sys.stdout = open ('/dev/pts/3', 'w')
#sys.stderr = open ('/dev/pts/3', 'w')
global lineNo
def lineNo():  return (str(sys._getframe(1).f_lineno) + ' ')


while(1):
    print sys.argv[0] # this is this scripts name
    print sys.argv[1] # this is the file we're going to butcher
#    print "len(sys.argv) " ,len(sys.argv)
    if len(sys.argv) < 2:
      print lineNo() + 'this script expects 2 arguments, the Callers name and the File Name'
      break
    if len(sys.argv[0]) < 10:
      print lineNo() + 'this script needs argv[0] filled in with with the callers name'
      break
    if len(sys.argv[1]) < 6:
      print lineNo() + 'this script needs argv[1] filled in with the File name'
      break
#    if sys.argv[1] != 'runScripts': # who cares
#      print lineNo() + 'argv[1] must be runScripts'
#      break
    print lineNo() + "qfx file being processed is ",sys.argv[1]
    fileName = sys.argv[1]
#    sys.argv = [''] # clean the arguments out.... why
    break
if fileName.count(".qfx") != 1 :
    print lineNo() + "This is not a .qfx file"
    sys.exit()

fin = open( fileName ,'r') # this is the qfx file we are going to process
outfileName = fileName.replace(".qfx",'-fixed.qfx') # if its not a .qfx file this will erase the file you just fed it....ie. outfile == fin ...Wiped out some of my .txt files.... ..................................
fout = open(outfileName ,'w') # this is the qfx file we are going to create

print lineNo() + "new qfx file will be named ",outfileName

timeZone = "[-5:EDT]" # only works on BMO files ... CIBC uses EST  .. Scotia uses MST .. Canadian tire use no Time Zone
while 1:
    sym = fin.readline()
    if not sym : break
#    print lineNo() + "len(sym) " , len(sym)
#    if len(sym) <= 50:
#      break
#    sym = sym.lstrip().rstrip() # remove trailing and proceeding garbage CR LF \r \n ' ' and spaces
#  sym = sym.replace(',',' ') # changes , to blanks.. don't do this'
#    lst = sym.split(',')      # removes the  ',' too.. not required
    if sym.count("<ACCTID>") > 0:
        account = sym
        account = account.replace("<ACCTID>",'')
        print lineNo() + "Found the Account #" ,account  # we could check if this is a valid BMO # account or not
    if sym.count("<DTPOSTED>") > 0 and sym.count(timeZone) > 0:
        print lineNo() + "Changing Time Zone on <DTPOSTED>"
        sym = sym.replace(timeZone,"[-8:PST]") # replace it with my timezone or maybe [-8:GMT]
    print lineNo() + sym
    fout.write(sym)
fin.close()
fout.close()
print "Done qfxStripper.py"


#    break
