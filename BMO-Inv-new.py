#!/usr/bin/env python
# coding: utf8
# version march 5 2025
# started by runScripts or ScotiaPicker which uses execfile with sys.argv = ['','runScripts','BMO RRSP TEST']  .. the account name is passed as argv[2]
#
#   see moneydance-API-doc.ods in Lessons/moneydance/Investment-Accounts
#   see Investment Transactions.ods in Lessons/moneydance/Investment-Accounts

class BMOInv:

  import sys
  import time
  from time import mktime , localtime ,strftime
#  from java.awt.event import ActionListener
#  sys.stdout = open ('/dev/pts/3', 'w') # this is not required because this script is normally started by runScripts.py or a console
#  sys.stderr = open ('/dev/pts/3', 'w') # this doesn't work . You still Need to check the moneydance Console
  global lineNo
  def lineNo():  return (str(sys._getframe(1).f_lineno) + ' ')

  execfile("/opt/moneydance/scripts/definitions.py")  # defines StockwatchSymbols, StockwatchIndexs and StockPriceHistoryStockwatch
  execfile("/opt/moneydance/scripts/AccountNames.py") # defines ScotiaAccounts and BMOAccounts
  execfile("/opt/moneydance/scripts/BMOdescTable.py") # defines BMOdescTable
  execfile("/opt/moneydance/scripts/BondTable.py")    # defines BondTable
  execfile("/opt/moneydance/scripts/ROClist.py")    # defines ROClist
  execfile("/opt/moneydance/scripts/Banktransactions.py")    # defines BANKtransactions


  csvfile = "~/Downloads/TransactionHistory.csv" # this is an example of where the default BMO csv file lives
  execfile("/opt/moneydance/scripts/selectBMOCsvfile.py") # execfile works .. select file to open .. file must be in /home/wayne/Downloads
  file3 = open('/opt/moneydance/scripts/tmp/selectBMOCsvfile.txt', 'rb') # this is where the selectBMOCsvfile.py script puts the selected .csv file name
  print lineNo() + " ", file3
  csvfile = file3.read() # get the selected csv file name to load
  file3.close()

  def lookupTicker(description,table): # table is a dictionary of lists
 #     print "The ticker symbol is missing, try Looking it up using the description "
    tickerSym = None
#    description = description[:25] #20 was too long
#    print lineNo()+"lookupTicker for", description
    for tickersym , tickerDesc in table.items(): # walk the dictionary
#        print "tickersym,tickerDesc",tickersym , tickerDesc # tickerDesc
#        print "len tickerDesc,len desc",len(tickerDesc),len(description)
        for x in tickerDesc: # look at all the Descriptions for a match
#                print "x ", x
                if  x.count (description) > 0:
#                  print lineNo()+"lookupTicker found it", tickersym ,x
	          tickerSym = tickersym
	          break
        if tickerSym is not None:
                print lineNo()+"lookupTicker found it ", tickersym
                break
#    if tickerSym == None:
#        print lineNo()+"lookupTicker failed"
    return tickerSym

# BondTable is a dictionary of dictionaries
  def lookupBondTicker(description,table):
    tickerSym = None
    description = description[:10] # only checking 10 characters
    for ticker in table:
#      print ticker, table[ticker]['desc']
      desc = table[ticker]['desc']
      if len(desc) <= 0: break
      if desc.count(description) > 0:
        print lineNo() + "lookupBond found it in the bond table", ticker
        tickerSym = ticker
        break
    return tickerSym

  def str2date(day,month,year): # Scotia Bank date format ... not used by this script
    from time import mktime , localtime
    monthss = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']    
#   month,day,year = date.strip().split('/')
    month = month.upper()
 #  print month
 #  print day
 #  print year
    index = monthss.index(month)
    index = index + 1
 #  print index	
    a=(int(year),index,int(day), 0, 0, 0, 0, 0, -1)
    x = mktime(a) # returns a float date-time number
    y = localtime(x) # returns a tuple of 9 elements like 'a' above . for use with strftime()
    return y
   
  def str2dateBMO(day,month,year):
    from time import mktime , localtime
#   month,day,year = date.strip().split('/')
 #  print month
 #  print day
 #  print year
    a=(int(year),int(month),int(day), 0, 0, 0, 0, 0, -1)
    x = mktime(a) # returns a float date-time number
    y = localtime(x) # returns a tuple of 9 elements like 'a' above . for use with strftime()
    return y
   
  def mdDate(dateStr):
    dates = dateStr.split('/')
    mm = dates[0]
    if len(mm) < 2:
      mm = '0' + mm
    dd = dates[1]
    if len(dd) < 2:
      dd = '0' + dd
    return int(dates[2] + mm + dd)

  def mdQty(qtyStr, decimals):
    l = len(qtyStr)
#  print 'qtyStr l decimals',qtyStr,l,decimals
    if l == 0:
      return 0
    neg = ''
    md = ''
    frac = ''
    newfrac = ''
    i = 0
    while i < l:
      c = qtyStr[i]
      i = i + 1
      if c == '(':
	neg = '-'
      elif c == '$' or c == ',' or c == ')' or c == '\n':
	pass
      elif c == '.':
	frac = qtyStr[i:i+decimals]
	i = 0
	while i < decimals:
	  if i >= len(frac):
	    break
	  c = frac[i]
	  if c == ')' or c == '\n':
#	  	print "frac c=)or \\n" , c
	    newfrac = newfrac + '0'
	  else:
#	  	print "frac c=",c
	    newfrac = newfrac + c
	  i = i + 1
	break
      else:
	md = md + c
#      	print 'mdQty md=' , md
    while len(newfrac) < decimals:
      newfrac = newfrac + '0'         
#  	print 'neg', neg # sign
#  print 'md' , md 
#  print 'newfrac',newfrac  
    x = int(neg + md + newfrac)
#    print 'mdQty returning integer=',x
    return x
  
# The currencies within Moneydance are held within a CurrencyTable. 
# This will be populated with all predefined currencies, 
# not just the ones you have selected. In addition there are entries for securities. 
# If one of your investment accounts holds shares for say, IBM, there will be a currency for IBM. 
#
# The account will have a balance of the number of shares and a currency of IBM.
# The data is accessed via theAccountBook, it is held as an array of CurrencyType. 
# There is a nested class called CurrencyType.Type that determines whether the CurrencyType is a currency or a security. 
  
   
  def getSecurityAcct(rootAcct, invAcct, tickerSym):
    import com.infinitekind.moneydance.model.Account
    import com.infinitekind.moneydance.model.CurrencyTable
    import com.infinitekind.moneydance.model.AccountBook
#    print("getSecurityAcct 234")
# below makes sure currencies.getCurrencyByTickerSymbol is never called with tickerSym = None .. it blows up with a Java Null pointer error
    if tickerSym is None:
      return None
    
 #   Rootaccount2 = getRootAccount() # test
 #   objAcctBook = extension.getUnprotectedContext().getCurrentAccountBook() #test
 #   CurrencyTable2 = objAcctBook.getCurrencies() # test
 #   rootAcct = moneydance.getRootAccount()
    AcctBook = rootAcct.getBook() 
    if AcctBook is None:
      print lineNo() + " rootAcct.getBook() failed"
      return None
    
    currencies = AcctBook.getCurrencies()
    if currencies is None: # or if not currencies or if currencies == None
      print lineNo() + " AcctBook.getCurrencies() failed"
      return None
 
#    currencies = rootAcct.getCurrencyTable() 
#   AttributeError: 'com.infinitekind.moneydance.model.Account' object has no attribute 'getCurrencyTable'
    curr = currencies.getCurrencyByTickerSymbol(tickerSym) # currency's and securities are treated the same way in moneydance ... this function blows if called with None ticker
#  the above crashes the program with java.lang.NullPointerException: java.lang.NullPointerException: Parameter specified as non-null is null: method
#  if the security is missing in the account need to wrap it in a try.....
    if curr is None:
      print lineNo() + "getSecurityAcct, Security not found ",tickerSym
      return None
# debug    print "curr ",curr #said PATHFINDER INCOME FUND PCD-UN 
#    sz = rootAcct.getSubAccountCount() # this one said 380 accounts
    sz = invAcct.getSubAccountCount() # says 15 , they are all the securities used by this investment account accoun
#debug    print "sz",sz
    i = 0
    for i in xrange(0,sz): 
      subAcct = invAcct.getSubAccount(i)
# debug     print "subAccount",subAcct.getAccountName()
#      if subAcct.getAccountType() == invAcct.AccountType.valueOf("SECURITY") :
#	print "its a SECURITY Type "     they are all SECURITY types
      if subAcct.getAccountType() != invAcct.AccountType.valueOf("SECURITY") :
	     continue # skip it if its not a SECURITY
      if subAcct.getAccountName() == curr.getName(): # the name of the subaccount matches the ticker symbols name
#         print "found it ",curr
         return subAcct
    print lineNo() + " Security not found ",tickerSym
    return None 
#    secAcctName = invAcct.getAccountName() + ':' + curr.getName() ..........this doesn't work anymore was wierd anyways
#    print "secAcctName",secAcctName
#    secAcct = rootAcct.getAccountByName(secAcctName)    
##    secAcct = AcctBook.getAccountByName(secAcctName)
#    if secAcct is None:
#      print "security (ticker) acct not found",secAcctName
#    return secAcct
#public java.util.List<Account> getSubAccounts(AcctFilter search) ######################## maybe could use this function instead of the for loop above
#Return a list of all accounts under this account matching the given filter. 
#This includes accounts not just direct children but all accounts under this one in the hierarchy.

    
#    New function for MD2015  
#    static ParentTxn 	makeParentTxn(AccountBook book, int date, int taxDate, long dateEntered, 
#             java.lang.String checkNumber, set to blank
#             Account account, 
#             java.lang.String description, 
#             java.lang.String memo, 
#             long id, -- set to -1 ??
#             byte status) -- set to unreconciled
#    Shortcut to create a ParentTxn object.

#static SplitTxn 	makeSplitTxn(ParentTxn parentTxn, 
#                        long parentAmount,            0          -amt
#                        long splitAmount,             0          -amt    
#                        float  rate,                  100         100
#                        Account account,              secAcct     incAcct
#                        java.lang.String description, desc        desc 
# -1 for new txn         long txnId,                   -1           -1
#                        byte status)                  unrec       unrec
# split parameter TAG_INVST_SPLIT_TYPE =        TAG_INVST_SPLIT_SEC   TAG_INVST_SPLIT_INC  TAG_INVST_SPLIT_EXP  TAG_INVST_SPLIT_FEE  TAG_INVST_SPLIT_TYPE   TAG_INVST_SPLIT_XFR
# parent setTransferType                 TRANSFER_TYPE_DIVIDEND  TRANSFER_TYPE_BUYSELL TRANSFER_TYPE_MISCINCEXP TRANSFER_TYPE_BUYSELLXFR TRANSFER_TYPE_BANK TRANSFER_TYPE_DIVIDENDXRF TRANSFER_TYPE_SHORTCOVER

#BANK              Moves cash from some other account to the cash of the investment account.
#see moneydance-API-doc.ods Cover/Short says 2 Splits .. looks like Buy/Sell  ? .. need to test
#    processTxnBMO(root,     invAcct , secAcct, transdate ,desc, memo,activity,Amount$,shares,Price,BrokerFee,ticker)

  global processTxnBMO
  def processTxnBMO(rootAcct, invAcct, secAcct, dateInt, desc, memo, action, amt, val, rate, BrokerFee, tickerSym, XferCategory):
    from com.infinitekind.moneydance.model import AbstractTxn
    from com.infinitekind.moneydance.model import ParentTxn
    from com.infinitekind.moneydance.model import SplitTxn
    from com.infinitekind.moneydance.model import TxnUtil
    from com.infinitekind.moneydance.model import InvestTxnType
    import time
#    from java.awt.event import ActionListener

    if rootAcct is None:
        print lineNo() + " Error processTxnBMO the rootAcct is missing"
        raise Exception (lineNo() + " processTxnBMO is Missing the rootAccount")

    if invAcct is None:
        print lineNo() + " Error processTxnBMO the invAcct is missing"
        raise Exception (lineNo() + " processTxnBMO is Missing the invAccount")

    if secAcct is None: # FAKE-T should already have been substituted in
        print lineNo() + " Error processTxnBMO the secAcct is missing"
        print "did you forget to add the security to your account ??"
        raise Exception (lineNo() + " processTxnBMO is Missing the secAccount")

#    XferCategory = "Unknown" #  used by BANK transactions. it could be an Account but isn't in this script'

    if action == '' or action == ' ' or action is None:
        print lineNo() + " We got a Blank action ", desc
#        if tickerSym == 'CSH-UN-T' or tickerSym == 'GRT-UN-T': # could be a ROC Return Of Capital, also the Quantity and Price should be zero
#        if lookupROC(tickerSym): # see if its in the list of stocks that post ROC div's'
        if tickerSym in ROClist: # see if its in the list of stocks that post ROC div's'
                print lineNo() + "its an ROC ",tickerSym
                action = 'ROC'
        else:
                memo = 'FAKE ACTION it WAS BLANK' + memo
                action = 'Interest' # taking a wild guess
                print lineNo() + "FAKING an Interest ACTION for tickerSym shares price:",tickerSym,val,rate
#        showMessage66(runScripts,"FAKE Action Interest it was BLANK") # if this fires during the 10 second sleep bad things happen
#        time.sleep (10)  # need some time to display the message

    if action == 'DivReinvest' :
        memo = action + memo
        action = 'DVF'

    if action == 'Cash in lieu' :  # showed up $7.58 on M&B TNT when it split 1 for 5.75
        memo = action + memo
        action = 'Dividend'

    if action == 'Redemption' :
        memo = action + memo
        action = 'Sell'
                               # a Buy or Sell with zero dollars drives moneydance nuts .. will post it as MiscInc with zero dollars
                               # may need to do a stock split manually later
    if action == 'Exchange' :  # usually a pure STOCK transaction BUY or SELL .. maybe a split .. normally two of them .. one with no ticker
        if decimals == 4:
          memo = action + ' FAKE ' +str(val/10000.0) + memo
        else: # must be 5
          memo = action + ' FAKE ' +str(val/100000.0) + memo
        action = 'MiscInc'
#        print lineNo() + 'val' + str(val) # its a float .. the neg sign was stripped off val .. val has been converted using number of decimal places already
#        if val > 0:
#          action = 'Buy'
#        else:
#          action = 'Sell'

    if action == 'Div' :
        memo = action + memo
        action = 'Dividend'

    if action == 'Dividend' and rate != 0 and val is not None and amt is not None  :  # MID436 transaction .. has Price(rate) and number of Stocks(val) and total amount(amt)
        print lineNo() + " We got a dividend reinvestment transaction for:",desc      # acts like a mutual fund
        memo = action + memo
        action = 'DVF' # dividend reinvest

#    if  action.count ('Transfer in') > 0:  # cash from some where
#        memo = action + memo
#        action = 'BANK' # this worked ok but the transfer account is missing .. just uses "unknown" .. shows up in the Bank Register :)

    if  action.count ('RRIF transfer') > 0:  # cash or stocks from some where .. Maybe Scotia
        memo = action + memo
        if val != 0: # has stocks
          action = 'Buy'
        else:
          action = 'BANK'

    if  action.count ('Disbursement') > 0:  # free stocks from some where maybe a corporate spin-off
        memo = action + memo
        if val != 0: # has stocks
          action = 'Buy'
        else:
          action = 'BANK'

#    if  action.count ('Contribution') > 0:  # cash from some where
#        memo = action + memo
#        action = 'BANK' # this worked ok but the transfer account is missing .. just uses "unknown" .. shows up in the Bank Register :)

#    if  action.count ('Payment') > 0:
#        memo = action + memo
#        action = 'BANK'
#        XferCategory = "LIF Pension"

#    if  action.count ('Federal tax') > 0:
#        memo = action + memo
#        action = 'BANK'
#        XferCategory = "Tax:Income Tax"

#    if  action.count ('De-registration fee') > 0:
#        memo = action + memo
#        action = 'BANK'
#        XferCategory = "Bank Fees"

#    if  action.count ('Withdrawal') > 0: # XferCategory could be Wife's Pension, My Pension ,  TFSA Pension etc....
#        memo = action + memo
#        action = 'BANK'
#        XferCategory = "M&B Pension"

#    if  action.count ('Goods & Services Tax') > 0:
#        memo = action + memo
#        action = 'BANK'
#        XferCategory = "Tax:GST"

#    if  action.count ('RSP fee paid') > 0:
#        memo = action + memo
#        action = 'BANK'
#        XferCategory = "Bank Fees"

    if  action.count ('Reinvestment') > 0:  # cash or stocks from some where like a DRIP
        memo = action + memo
        if val != 0: # has stocks
          action = 'Buy'
        else:
          action = 'BANK'

    if action == 'Interest'or action == 'Dividend' or action == 'ROC': # negative dividends are a big problem .. you will have to delete two transactions manually from your account
      if amt < 0:
        print lineNo() + " processTxnBMO Interest/Dividend amount is negative", amt/100.0 #moneydance dosen't handle negative dividends properly .. need to switch to MiscExp
        print lineNo() + " switching it to MiscExp" #Granite and Brookfield both have used negative Interest dividends to correct errors
        memo = action +' FAKE ' +memo
        action = 'MiscExp'

# ..............................................................................from here down the remapping of actions should be complete
    AcctBook = rootAcct.getBook()                  #2015-1
    txnSet = AcctBook.getTransactionSet()          #2015-2 
    Partxn = ParentTxn.makeParentTxn(AcctBook,dateInt, dateInt, dateInt, "", invAcct,  desc, memo, -1, AbstractTxn.STATUS_UNRECONCILED) #2015
    if action == 'Buy' or action == 'Sell' or action == 'Short' or action == 'Cover':                       # don't need an inc split because it doesn't effect your income
#      print 'BUY/SELL amt=',amt # 15000 = $150.00 total value of transaction (long ) 2 decimals
#      print 'BUY/SELL val=',val # 1000000 =  100 number of stocks (long ) 4 decimals # Quantity .. maybe 5 on some stocks  .. maybe negative (Sell)
#      print 'BUY/SELL rate=',rate # price 840.0 = $8.40  (float)  2 decimals         # Price
#      print 'BUY/SELL BrokerFee =',BrokerFee # fee 840.0 = $8.40 (float) 2 decimals
      if action == 'Sell':
	 TxnUtil.setInvstTxnType(Partxn,InvestTxnType.SELL) # below needs to be tested on a BMO SELL .. march 1 2025
         secSplit = SplitTxn.makeSplitTxn(Partxn, long (amt - BrokerFee) , long(val* -1.0), rate , secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #SELL
      elif action == 'Buy':
	 TxnUtil.setInvstTxnType(Partxn,InvestTxnType.BUY) # BMO BUY amt is negative   #stocks   Price
         secSplit = SplitTxn.makeSplitTxn(Partxn, long ((amt + BrokerFee )* -1.0 ), long(val), rate, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #BUY
      elif action == 'Short': # Shorts and Covers don't belong in this account,should be kept in a different account until they are ripe ... just here for error handling
         TxnUtil.setInvstTxnType(Partxn,InvestTxnType.SHORT)
         secSplit = SplitTxn.makeSplitTxn(Partxn, long ((amt + BrokerFee )* -1.0), long(val), rate, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #Short (Sell)
      elif action == 'Cover': # just here for error handling .. Cover needs a different account number
	 TxnUtil.setInvstTxnType(Partxn,InvestTxnType.COVER)
         secSplit = SplitTxn.makeSplitTxn(Partxn, long (amt - BrokerFee ), long(val* -1.0), rate, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #Cover (Buy)

      TxnUtil.setSecurityPart(secSplit)
      Partxn.addSplit(secSplit)
      feeAcct = None  
      feeAcct = rootAcct.getAccountByName('Fees Broker')
      if feeAcct is None:
        print lineNo() + " no catagory Fees Broker"
        return     
      feeSplit = SplitTxn.makeSplitTxn(Partxn, long (BrokerFee) ,0,0, feeAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #fees
      TxnUtil.setCommissionPart(feeSplit)
      Partxn.addSplit(feeSplit)      

    elif action == 'BuyXfr' or action == 'SellXfr':
      print lineNo() + " BuyXfr and SellXfr are Unimplemented"
      print lineNo() + " Just use a BANK plus Buy or Sell"
      showMessage66(runScripts,"Unimplemented Action BuyXfr or SellXfr")
      raise Exception (lineNo() + " processTxnBMO Unimplemented BuyXfr or SellXfr")
      #........................................... not doing anything for BuyXfr and SellXfr ... just use BANK and Buy or Sell

    elif action == 'Dividend': # BMO also provides the number of shares which is not used .. no fees
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.DIVIDEND)
      secSplit = SplitTxn.makeSplitTxn(Partxn, 0, 0, 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED) #2015 secAcct is for the ticker symbol stats
      TxnUtil.setSecurityPart(secSplit)
      Partxn.addSplit(secSplit)
      autoAcct = rootAcct.getAccountByName('Dividend Income') # looks up an income catagory
      if autoAcct is None:
        print lineNo() + " no catagory called Dividend Income"
        return
      incSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED) #autoAcct is the income catagory
      TxnUtil.setIncomePart(incSplit)
      Partxn.addSplit(incSplit)
    elif action == 'ROC': # Return of Capital .. no fees
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.DIVIDEND)
      secSplit = SplitTxn.makeSplitTxn(Partxn, 0, 0, 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED) #2015 secAcct is for the ticker symbol stats
      TxnUtil.setSecurityPart(secSplit)
      Partxn.addSplit(secSplit)
      autoAcct = rootAcct.getAccountByName('Return of Capital') # looks up an income catagory
      if autoAcct is None:
        print lineNo() + " no catagory called Return of Capital"
        return
      incSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED) #autoAcct is the income catagory
      TxnUtil.setIncomePart(incSplit)
      Partxn.addSplit(incSplit)
    elif action == 'Interest': # BMO also provides the number of shares which is not used .. no fees
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.DIVIDEND)
      secSplit = SplitTxn.makeSplitTxn(Partxn, 0, 0, 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)
      TxnUtil.setSecurityPart(secSplit)
      Partxn.addSplit(secSplit)
      autoAcct = rootAcct.getAccountByName('Interest Income') # Interest is taxable
      if autoAcct is None:
        print lineNo() + " no catagory called Interest Income"
        return
      incSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED)
      TxnUtil.setIncomePart(incSplit)
      Partxn.addSplit(incSplit)

# A DivReinvest has 3 splits 1-security secSplit 2-incSplit or expSplit(shows as Category) 3-optional Fee Category .. feeSplit
    elif action == 'DVF': # dividend reinvestment .. has stocks(val) .. Price(rate)(optional) and total amount(amt) , no fees  ..
# the Price(rate) gets changed by moneydance to keep the amt(cash) and val(shares) as specified
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.DIVIDEND_REINVEST)
      secSplit = SplitTxn.makeSplitTxn(Partxn, long(amt), long(val), rate, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED) # removed the BrokerFee
#      secSplit = SplitTxn.makeSplitTxn(Partxn, long(amt), long(val), 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)   # this works too .don't really need the Price
      TxnUtil.setSecurityPart(secSplit)
      Partxn.addSplit(secSplit)
      autoAcct = rootAcct.getAccountByName('Dividend Income') # looks up the income catagory
      if autoAcct is None:
        print lineNO() + " DVF no category called 'Dividend Income'"
        return
      incSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED)
      TxnUtil.setIncomePart(incSplit)
      Partxn.addSplit(incSplit)

    elif action == 'MiscInc':    # we could have no security to go with this income maybe just interest on cash in the account
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.MISCINC)
      if secAcct is not None:    # must have found a ticker
         secSplit = SplitTxn.makeSplitTxn(Partxn, 0, 0, 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)
         TxnUtil.setSecurityPart(secSplit)
         Partxn.addSplit(secSplit)
      autoAcct = None  
      autoAcct = rootAcct.getAccountByName('Interest Income') # a catagory
      if autoAcct is None:
        print lineNo() + " no catagory called Interest Income"
        return
      incSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED)
      TxnUtil.setIncomePart(incSplit)     
      Partxn.addSplit(incSplit)



    elif action == 'MiscExp':    # we could have no security to go with this expense maybe just more bank fees. the amt sign needs to be negitive in the csv file
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.MISCEXP)
      if secAcct is not None:    # must have found a ticker
         secSplit = SplitTxn.makeSplitTxn(Partxn, 0, 0, 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)
         TxnUtil.setSecurityPart(secSplit)
         Partxn.addSplit(secSplit)
      autoAcct = None  
      autoAcct = rootAcct.getAccountByName('unknown') # a catagory
      if autoAcct is None:
        print lineNo() + " no catagory called unknown"
        return
      expSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED)
      TxnUtil.setExpensePart(expSplit)     
      Partxn.addSplit(expSplit)

    elif action == 'BANK' : # no fees XferCategory is a global category like "tax:GST"
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.BANK)
      autoAcct = rootAcct.getAccountByName(XferCategory)
      if autoAcct is None:
              print lineNo() + " no catagory called ", XferCategory
###        return # should default to Unknown
      xfrSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED)
      TxnUtil.setXfrPart(xfrSplit)
      Partxn.addSplit(xfrSplit)       # fills in the "Transfer" account name with "Bank Fees" etc..
# assume there are no  Fees  on a BANK transfer will default to unkown should set it to Fees Broker too
    else: 
      print lineNo() + " Error Unknown action", action # this is a big deal you will need to edit this script
      print lineNo() + " Desc ",desc
      print lineNo() + " secAcct ",secAcct
#      global showMessage66
      showMessage66(runScripts,"Unknown Action Faking a Short ")
      memo = 'Fake Short Action was '+ action +' ' + memo
      time.sleep (10)  # need some time to display the message
      processTxnBMO(rootAcct, invAcct, secAcct, dateInt, desc, memo,'Short', amt, val, rate, BrokerFee, tickerSym, 'Unknown') # try recursion
#      raise Exception ('Unknown Action',action)
      return
    txnSet.addNewTxn(Partxn)
    time.sleep (0.100)  # seems to have fixed the thread crashs ... its in seconds ,,,, 100 milliseconds
#.........................................end of processTxnBMO function
#  raise Exception('I know Python!')
# .........................................................This Script continues execution from here

    
  print lineNo() + " BMO-Inv-new.py reading transactions from ",csvfile
  accountName = None
  while(1):
    if len(sys.argv) < 2:
      print lineNo() + ' this script needs 2 arguments to run'
      break
    if len(sys.argv[0]) < 10:
      print lineNo() + ' this script needs argv[0] filled in with the caller name'
      break
    if len(sys.argv[1]) < 10:
      print lineNo() + ' this script needs argv[1] filled in with the Account Name'
      break
#    if sys.argv[1] != 'runScripts':
#      print lineNo() + ' argv[1] must be runScripts'
#      break
    print lineNo() + " accountName is ",sys.argv[1]
    accountName = sys.argv[1]
#    print sys.argv[1] 
#    print sys.argv[2]
    sys.argv = [''] # clean the arguments out.
    break  
  
  if accountName is None:
      print lineNo() + " We need an Account Number"
      raise Exception (lineNo() + ' We need an Account Number')

  root = moneydance.getRootAccount()

  fin = open( csvfile ,'r') # this is the csv file we are going to process

  sym = fin.readline()                 #read the first line and throw it away ..  file starts with ef bb  bf .. or its "EF BB BF" means UTF-8
                                       # What you are seeing is the BOM (Byte Order Mark) - it indicates this is a Unicode file (UTF-8 in this case, I believe).
  print lineNo() +" HEADER1",sym
  sym = fin.readline()                 #read the second line and throw it away
  print lineNo() +" HEADER2",sym
  sym = fin.readline()                 #read the third line and throw it away
  print lineNo() +" HEADER3",sym



  while 1:
    sym = fin.readline()
    if len(sym) <= 50:
      break
#  sym = sym.replace(',',' ') # don't change the ',' to blanks
    sym = sym.lstrip().rstrip() # remove trailing and proceeding garbage CR LF \r \n ' ' and spaces
    lst = sym.split(',')        # this removes the  ',' too
    print lineNo() + " lst", lst
    
# Note BMO has hidden the fee in the "Total Amount" and moneydance adjusts the price to compensate. Messes things up
# so the amt passed to moneydance needs to be "Total Amount" + Fee and the Fee needs to be calculated and updated
# moneydance displays the amt - the fee so if you add the fee to it on a "SELL" it works out. On a "Buy" it should be the opposite.
# the amt passed to moneydance needs to be the result of the sale or purchase without the fee.
# "Fees Broker" is a good category/Account for the fees
# sample of the BMO investor line csv file layout.Note that the symbol is missing on one transaction . also the account #
#Transaction Type=All	Product Type=All	Period=	From=2017-12-01	To=2018-03-15
# note that the memo field is missing from the csv file .. it shows in the statement with like 4 lines of text in the Desc field .. where did it go ?
# The desc seems to be just the first line on the statement .
#Transaction Date	Settlement Date	Activity Description	Description	              Symbol	Quantity	Price	Currency	Total Amount	Currency
#----------------	---------------	--------------------	-----------	              ------	--------	-----	--------	------------	--------
#2018-03-01     	2018-03-01	      Dividend	        CDN UTIL 4.5% CUM RDM SECND PR	CU.PR.F	  700		                          196.88	CAD
#2018-01-15	        2018-01-17	        Buy	        EXCHANGE INC CORP	         EIF	  400	         33.25	    CDN	        -13309.95	CAD
#2018-01-15	        2018-01-15	      Interest	        REIT INDEXPLUS INC FD TR UNITS	IDR.UN	  1000			                      65	CAD
#2017-12-14	        2017-12-14	      Redemption	1000THS CANOE CDN ASSET ALLOC		  -862			                       0        CAD
#2017-12-12	        2017-12-14	        Sell	        CANOE CDN ASSET ALLOC CL SR Z(	GOC309	 -5529	          9.436	     CDN	  52179.78	CAD
# sample of the Scotia csv file layout.
#Description	                                                           Symbol  Transaction Date	Settlement Date	Account Currency	Type	Quantity	Currency of Price	Price	Settlement Amount
#PATHFINDER INCOME FUND TR UNIT DIST ON 1000 SHS REC 01/31/18 PAY 02/15/18 PCD.UN  15-Feb-2018	        15-Feb-2018     	  CAD	      CASH DIV	   0	          CAD	                 0	 50

#    print 'Tranaction Date=',lst[0]
#    print 'Settlement Date=',lst[1]
#    print 'Activity=',lst[2]
#    print 'Description=',lst[3]
#    print 'Symbol=',lst[4]
#    print 'Quantity=',lst[5]
#    print 'Price=',lst[6]
#    print 'Currency of Price=',lst[7]
#    print 'Total Amount=',lst[8]
#    print 'Currenty of Amount =',lst[9]
    
#  dateInt = mdDate(row['Date'])

# ..........................................................  Date
    try:
      transdate = lst[0].split('-')
      day = transdate[2]
      month = transdate[1]
      year= transdate[0]
    except IndexError as err:
      print lineNo() + "Got an IndexError on date"
      print lineNo() + "Looks like this is not a BMO csv file"
      raise Exception (lineNo() + "Looks like this is not a BMO csv file")
#    print 'day=',day
#    print 'month=',month
#    print 'year=',year

    date = str2dateBMO ( day,month,year )
    transdate = int (strftime("%Y%m%d",date)) # 20120130
#    print transdate

#    invAcct = root.getAccountByName(runScripts.accountName)
    invAcct = root.getAccountByName(accountName)
    if invAcct is None:
      print lineNo() + " BMO-Inv-new.py missing the name of the Moneydance Investment account to update"
      print lineNo() + " accountName=", accountName
      break
# fill in the memo field with something useful since its missing in the csv file
# all subsequent memo entries should be memo = memo + "something"
# its used as a way to communicate with the user of this script

#    memo = 'BMO-Inv-new.py'
    import datetime

    t = datetime.datetime.now()
    memo = t.strftime(' %m/%d/%Y-%I-%M-%S ')

#    print ("720 memo",memo)
#    print (x)
#    print(x.year)
#    print(x.month)
#    print(x.day)
#    print(x.hour)
#    print(x.minute)
#    print(x.second)

#    raise Exception ('Testing')
#............................................................Action
    Action = lst[2]
    Action = Action.strip() # had some trailing blanks on some BANK actions

# ...........................................................Description
    Description = lst[3]
    
# ...........................................................tickerSym
    secAcct = None
    tickerSym = lst[4]
    tickerSym = tickerSym.strip() # remove the single bloody 0x20 char
#    print lineNo() + "tickerSym len,Sym",len(tickerSym),tickerSym # for some reason len was 1 .. it was a single space 0x20
#    if (tickerSym == ' '):
#      print lineNo() + "tickerSym is a single blank char 0x20" # didn't get this message after the strip()'
#    if (tickerSym == ''):
#      print lineNo() + "tickerSym is an empty string "  # after the strip we got this message
#    if (tickerSym is None):
#      print lineNo() + "tickerSym is None"   # we didn't get this message so '' is different than None

#    if (len(tickerSym) <= 0) | (tickerSym == ' '):  # this was a bit wise or oh dear ???
    if (len(tickerSym) <= 0) or (tickerSym == ' '): # len of '' is zero
#      print lineNo() + "setting tickerSym to None"
      tickerSym = None
    else: # we got a good one
      tickerSym = tickerSym.replace('.','-') 
      tickerSym = tickerSym+"-T" #  what about the other stock exchanges
      for tsxSym ,NYXSym in definitions.ExchangeTable.items():  #check to see if this symbol is on a different stock exchange then the TSX
#        print tsxSym , NYXSym
#        print len(NYXSym)
	if len(NYXSym) <= 0: break
	if  tsxSym == tickerSym:
	  print lineNo() + " Not on the TSX", tsxSym ,NYXSym
	  tickerSym = NYXSym
#          print "new tickerSym=",tickerSym
	  break

      
#    print lineNo() + 'ticker ',tickerSym
    XferCategory = 'Unknown' # will get changed by BANKtransactions[Action]
    if tickerSym is not None:
      secAcct = getSecurityAcct(root, invAcct, tickerSym)
      if secAcct is None:
         print lineNo() + "Maybe this security needs to be added to the account " , tickerSym
         print lineNo() + " Using Fake-T  for now"
         secAcct = getSecurityAcct(root,invAcct,"FAKE-T") # just fake it
         if secAcct is None:
	   raise Exception ('Security FAKE-T is missing, add it to your account')
         memo = "using FAKE-T" + memo
    else:# the ticker is None  .. BANK transactions don't need a ticker
      if Action not in BANKtransactions:
        print lineNo() + " Missing ticker symbol, will try Looking it up in the BMOdescTable "
        tickerSym = lookupTicker(Description,BMOdescTable) # try's to find the ticker in the BMOdescTable using the BMO Description
        if tickerSym is None:
              print lineNo() + "lookupTicker failed. will Try the BondTable next"
              tickerSym= lookupBondTicker(Description,BondTable) # bonds never have a tickers
              if tickerSym is None:
                 print lineNo() + "lookupBondTicker failed. ticker is still None"
                 print lineNo() + "Cannot find a ticker will use FAKE-T"
                 secAcct = getSecurityAcct(root,invAcct,"FAKE-T") # just fake it
                 if secAcct is None:
	             raise Exception (lineNo() + 'Security FAKE-T is missing, add it to your account')
	      else:
	         print lineNo() + "lookupBondTicker found a ticker"
                 secAcct = getSecurityAcct(root,invAcct,tickerSym)
                 if secAcct is None:
	            raise Exception (lineNo() + 'Security is missing, add it to your account ',tickerSym)
        else:
#              print lineNo() + "lookupTicker found a ticker"
              secAcct = getSecurityAcct(root,invAcct,tickerSym)
              if secAcct is None:
	         raise Exception (lineNo() + 'Security is missing, add it to your account ',tickerSym)
      else: # its a BANK transaction so just fake the ticker . its not needed but
        secAcct = getSecurityAcct(root,invAcct,"FAKE-T") # just fake it
        if secAcct is None:
           raise Exception (lineNo() + 'Security FAKE-T is missing, add it to your account')
        XferCategory = BANKtransactions[Action] # set the global BANK xferCategory
        memo = Action + memo # before we wipe the Action out
        print lineNo() + "This is a BANK transaction", Action
        Action = 'BANK'

#.........................................Quantity......Shares.....val............................................................
    global decimals # applies to the stock Quantity
    decimals = secAcct.getCurrencyType().getDecimalPlaces() # securities (stocks) are stored with 4 decimal places
#    userRate = secAcct.getCurrencyType().getUserRate()
#    print '759 decimals used for Stock Quantity' ,decimals
    if decimals != 4 and decimals != 5:
      print lineNo() + ' decimals are:', decimals
      raise Exception (lineNo() + ' Decimals must be 4 or 5')
#    print 'UserRate used for Stock Quantity' ,userRate
    if decimals == 4:
      Quantity = mdQty(lst[5], 4 )  # in csv file, buy is > 0, sell is < 0  #number of stocks , BMO may have 4 decimal places (mutual funds)

    if decimals == 5:
      Quantity = mdQty(lst[5], 5 )

##    if Quantity < 0:
##      Quantity = Quantity * (-1.0)      # let the BUY / SELL action decide on the + or - sign

#    print '780 Quantity decimals',Quantity , decimals

#...................................Price .......................................................................................................................
    Price = mdQty(lst[6], 4 )  # the price could have up to 4 decimal places in the csv .. the csv file has 11.3883 in it ... only middlefield has 4 places
#    print '784 Price', Price   # 113883  .. moneydance uses doubles for price
    PriceRaw = Price / 100.0   # money dance only uses 2 decimal places on price so drop 2 places and convert to float
#    print '786 PriceRaw', PriceRaw   # 1138.83   .. this shows the round off error .83 will be dropped BMO uses 4 decimal places on price.
#    print '787 % the fraction ', Price % 1   # just the fraction .83
#    print '788 // the integer ', Price // 1   # the integer 1138
    if (PriceRaw % 1 ) != 0 :
       print lineNo() + ' BMO is using more than 2 decimals on Price'
#    if (PriceRaw % 1) > .5 :
#       print '793 Round off error detected'
#       Price = Price + 1
    Price = PriceRaw // 1 # just keep the integer part
    if Price < 0:
      Price = Price * (-1.0)
#    print '797 Price', Price

#.................................................Amount........................................................................................................
    Amount4 = mdQty(str(lst[8]), 4) # in csv file, buy is > 0, sell is < 0 . This is the "Settlement Amount" in dollars
                                    # ?????  both BMO and moneydance only use 2 decimal places on the Amount(total cost in Canadian Dollars)
    AmountRaw = Amount4 / 100.0 # drop 2 places and convert to float .. moneydance only uses 2 places for amount
    if ( AmountRaw % 1 ) != 0:
       print lineNo() + ' BMO is using more than 2 decimals on Amount(dollars)'

#    print '727 AmountRaw 2 places', AmountRaw
    Amount = AmountRaw // 1 # only want the integer .. get rid of any decimal value
#    print '816 Amount 2 places', Amount
#.................................................Broker Fee
# try to figure out what the Broker fee for the transaction was since its not included in the csv file data
# BELOW ONLY WORKS IF YOU HAVE A PRICE AND A QUANTITY(number of shares)
    if decimals == 4:
        AmountCalc = (float(Quantity)/10000) * (float(PriceRaw))  #Quantity is the number of shares * 10000 ..
    if decimals == 5:
        AmountCalc = (float(Quantity)/100000) * (float(PriceRaw))
#    BrokerFee = 0.0
    if AmountRaw < 0:
        testAmount = AmountRaw *(-1) # if its negative ... make it positive ???
    else:
        testAmount = AmountRaw
#    print '821 AmountCalc' , AmountCalc # 4146.48003
#    print '822 testAmount' , testAmount # 4146.48
        
    if testAmount < AmountCalc:
	BrokerFee =  AmountCalc - testAmount
    else:
	BrokerFee =  testAmount - AmountCalc
#    print'836 BrokerFee ', BrokerFee # 3.0000000 e-05
    if BrokerFee < 0:
        BrokerFee = BrokerFee *(-1)
    if Price == 0.0 or Quantity == 0 or BrokerFee < 1:
        BrokerFee = 0.0
#        print "841 BrokerFee Set to Zero"
#    if BrokerFee < 1 :
#        BrokerFee = 0.0
#        print "837 BrokerFee Set to Zero"

      
#    print '870 Price 2 decimals' ,Price # 1500  for $15.00
#    print '870 Stock Quantity 4 decimals' ,Quantity # shares 30000 for 3 ... if 5 decimals its 300000 for 3
#    print '870 Transaction Amount 2 decimals' ,Amount # total $ -450995 for -$4509.95 negative because its a buy
#    print '870 transdate' , transdate # 20230706 for july 6 2023
#    if (BrokerFee != 0):
#        print '843 BrokerFee 2 decimals' , BrokerFee # 995 is $9.95
#    raise Exception ('Testing')
    

#   processTxnBMO(rootAcct, invAcct,    secAcct, dateInt,    desc,       memo, action, amt,     val,      rate  , BrokerFee , tickerSym):
    processTxnBMO(root,     invAcct ,   secAcct, transdate ,Description, memo, Action , Amount,  Quantity, Price , BrokerFee , tickerSym , XferCategory)
#    raise Exception('I know Python!')    
  # while read csv file loop ends here
#######  root.refreshAccountBalances()  #not in 2015
  fin.close()
  import os
  os.rename(csvfile, csvfile + '-done')
  AcctBook = root.getBook() 
  AcctBook.refreshAccountBalances()
  print lineNo() + " Done BMO-Inv-new.py"
#................................................................................script execution ends here
