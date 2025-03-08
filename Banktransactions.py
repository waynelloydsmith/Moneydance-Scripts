#!/usr/bin/env python
# coding: utf8
# version march 5 2025

global BANKtransactions

# items in this list only have four things defined in the csv file Date,Action,Desc and Amount
# so if the ticker,Stock,Price are defined don't put them in this list.'
# its a python dictionary
# Action:XferCategory
BANKtransactions = {
   'Payment':'LIF Pension',
   'Federal tax':'Tax:Income Tax',
   'Contribution':'Unknown',
   'De-registration fee':'Bank Fees',
   'Withdrawal':'M&B Pension',
   'Goods & Services Tax': 'Tax:GST',
   'RSP fee paid':'Bank Fees',
   'Transfer in':'Unknown'
   }

# there are a lot of BANK transactions .. they all have no ticker .. so to #save time looking for a missing ticker just list them here
# if the action is in this list don't bother looking for a ticker
# in the BONDtable or DescTable etc.
# also this gets rid of the global XferCategory which we can put in this #dictionary too

#some examples of how to use the dictionary
##if "Payment" in BANKtransactions: print "True" # prints True
##else: print "False"
##print BANKtransactions["Payment"] # prints LIF Pension
##if "Jake" in BANKtransactions: print "True"
##else: print "False" # prints False
##try:
##  print BANKtransactions["Jake"] # fails
##except KeyError as e:
##  print "Jake is not in the Dictionary ", e

# prints 'Jake is not in the Dictionary  'Jake''


