#!/usr/bin/env python
# coding: utf8
# version March/2/2025

# these descriptions must match what BMO Investor line uses ... not what moneydance uses.. or stockwatch uses
#In Python, a dictionary doesn't allow duplicate keys or repeated keys.
# this table is far from complete. see ScotiaDescTable.py for a more complete example.
global BMOdescTable
#  because there are multiple descriptions for some tickers the simple dictionary does not work
# a dictionary of lists does
BMOdescTable = dict({
    'BEPC-T'  :['BROOKFIELD RENEWABLE CL A SUB','BROOKFIELD RENEWABLE NEW CL A','BROOKFIELD RENEWABLE CORP'],
    'BEP-UN-T':['BROOKFIELD RENEWABLE PARTNERS LP'],
    'CHR-T'   :['CHORUS AVIATION VTG & VAR VTG','CHORUS AVIATION COM VTG & VAR','CHORUS AVIATION INC'],
    'PIC-A-T' :['PREMIUM INCOME CORP CL A'],
    'TNT-UN-T':['TRUE NORTH COMMERCIAL RL EST INVMT TR'],
    'GRT-UN-T':['GRANITE REAL ESTATE INVESTMENT TRUST']
    })



# some testing of a dictionary of lists
#if 'CHR-T' in BMOdescTable : print 'True' # prints True
#if 'BROOKFIELD' in BMOdescTable.values() : print 'True2' # didn't print' the string is too short
#if 'BROOKFIELD RENEWABLE CORP' in BMOdescTable.values() : print 'True3' # didn't print' string is still too short
#if any('BROOKFIELD RENEWABLE CORP' in val for val in BMOdescTable.values()) : print 'YES' # printed YES
#keys = [key for key, value in BMOdescTable.items() if 'BROOKFIELD RENEWABLE CORP' in value] # I guess you could have the same desc on more than one key
#print keys # printed a list ['BEPC-T']

#for key, value in BMOdescTable.items():
#  if 'BROOKFIELD RENEWABLE CORP' in value:
#    print "key ", key                      # printed key  BEPC-T   .........WORKS
#    break

#for key, value in BMOdescTable.items():
#  if 'BROOKFIELD' in value:
#    print "key2 ", key                      # didn't print .. so it needs to match the whole string'
#    break

#for key, value in BMOdescTable.items():
#  if 'BROOKFIELD RENEWABLE CORP ' in value:
#    print "key3 ", key                      # didn't print either 'in' is same as ==
#    break

#for key, value in BMOdescTable.items():
#  if 'BROOKFIELD' any value:    # SyntaxError: no viable alternative at input 'any'
#    print "key4 ", key
#    break

#for key, value in BMOdescTable.items():
#  if any ( 'BROOKFIELD' in value ):  # TypeError: 'bool' object is not iterable
#    print "key5 ", key
#    break

#if any( 'BROOKFIELD RENEWABLE CORP' in value for key, value in BMOdescTable.items()):
#  print "true6 " , key  # printed true6  TNT-UN-T .. this almost worked but the key got lost in the scan

