#!/usr/bin/env python
# coding: utf8
# version 2/19/2025

# stocks that may issue ROC dividends as blank actions
# its a simple list
global ROClist

ROClist = ["GRT-UN-T", "CSH-UN-T", "cherry"]

#global lookupROC
#def lookupROC (ticker):
#        for x in ROClist: # scan the list
#            print "x ", x
#            if  x.count (ticker) > 0:
#                  print "yes its in the list"
#	          return True
#        return False

#if lookupROC("GRT-UN-T"): print "True"
#else: print "False"
# how about just using
# if ticker in ROClist
