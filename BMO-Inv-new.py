#!/usr/bin/env python
# coding: utf8
# started by runScripts which uses execfile with sys.argv = ['','runScripts','BMO RRSP TEST']  .. the account name is passed as argv[2]
# see Lessons/moneydance/moneydance-API-doc.ods

class BMOInv:

  import sys
  import time
  from time import mktime , localtime ,strftime
  from java.awt.event import ActionListener

  execfile("/opt/moneydance/scripts/definitions.py")


  csvfile = "/home/wayne/Downloads/TransactionHistory_21830908.csv" # this is an example of where the default BMO csv file lives
  execfile("/opt/moneydance/scripts/selectBMOCsvfile.py") # execfile works .. select file to open .. must be in /home/wayne/Downloads
  file3 = open('/opt/moneydance/scripts/tmp/selectBMOCsvfile.txt', 'rb') # this is where the selectBMOCsvfile.py script put the selection
  print"19 ", file3
  csvfile = file3.read()
  file3.close()





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
 
    
 #   Rootaccount2 = getRootAccount() # test
 #   objAcctBook = extension.getUnprotectedContext().getCurrentAccountBook() #test
 #   CurrencyTable2 = objAcctBook.getCurrencies() # test
 #   rootAcct = moneydance.getRootAccount()
    AcctBook = rootAcct.getBook() 
    if AcctBook is None:
      print "131 rootAcct.getBook() failed"
      return None
    
    currencies = AcctBook.getCurrencies()
    if currencies is None:
      print "136 AcctBook.getCurrencies() failed"
      return None
 
#    currencies = rootAcct.getCurrencyTable() 
#   AttributeError: 'com.infinitekind.moneydance.model.Account' object has no attribute 'getCurrencyTable'
    curr = currencies.getCurrencyByTickerSymbol(tickerSym) # currency's and securities are treated the same way in moneydance
    if curr is None:
      print "143 Security not found ",tickerSym
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
    print "160 Security not found ",tickerSym
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

#Creates a SplitTxn with the parentAmount having a negative effect on the account of parentTxn, and splitAmount having a positive effect on the account of this SplitTxn.
# see the spread sheet "Investment Transactions.ods"
# IvestTxnType --- not coded yet --- , SHORT, COVER, DIVIDENDXFR,
#SHORT             Removes shares of a security and adds cash to the investment account.
#COVER             Removes cash from investment account and converts to shares of a security.
#DIVIDENDXFR       Adds cash to some other account.
#BANK              Moves cash from some other account to the cash of the investment account.
#see moneydance-API-doc.ods Cover/Short says 2 Splits .. looks like Buy/Sell  ? .. need to test
#    processTxn(root,     invAcct ,   secAcct, transdate ,desc, memo,activity, Total-Amount$, shares Quantity, Price , BrokerFee)

  global processTxn
  def processTxn(rootAcct, invAcct, secAcct, dateInt, desc, memo, action, amt, val, rate, BrokerFee, tickerSym):
    from com.infinitekind.moneydance.model import AbstractTxn
    from com.infinitekind.moneydance.model import ParentTxn
    from com.infinitekind.moneydance.model import SplitTxn
    from com.infinitekind.moneydance.model import TxnUtil
    from com.infinitekind.moneydance.model import InvestTxnType
    import time
    from java.awt.event import ActionListener

#    print("259 amt",amt) #was negative
#    print("260 action",action) #was interest
#    raise Exception ('Testing')

    def showMessage66 (self,message) :
        #  mframe = JFrame("Message")
        global mframe66
        mframe66 = self.JFrame(message)
#       mframe.setSize(1000, 100)
        mframe66.setSize(1000, 50)
        mframe66.setDefaultCloseOperation(self.WindowConstants.DISPOSE_ON_CLOSE)
        mpnl = self.JPanel()
        mframe66.add(mpnl)
        mlabel = self.JLabel(str(message))
        mpnl.add(mlabel)
        mlabel.setVisible(True)
        mframe66.setVisible(True)
        self.WindowClose66()  # this is defined as a class in runScripts.py

    def __init__(self):
        from javax.swing import Timer
        self.timer = Timer(5000, self)
        self.timer.start()
    def actionPerformed(self, e):
        self.timer.stop()
        mframe.dispose()
        mframe.setVisible(True)
        self.WindowClose66()

    if rootAcct == None:
        print "245 Error processTxn the rootAcct is missing"
        raise Exception ("processTxn is Missing the rootAccount")

    if invAcct == None:
        print "249 Error processTxn the invAcct is missing"
        raise Exception ("processTxn is Missing the invAccount")

    if secAcct == None:
        print "253 Error processTxn the secAcct is missing"
        print "did you forget to add the security to the account ??"
        raise Exception ("processTxn is Missing the secAccount")

    XferCategory = "Unknown" # or XferAccount

    if action == '' or action == ' ':
        print "282 We got a Blank action",desc
        memo = 'ACTION WAS BLANK'
        action = 'Interest'
        print "263 tickerSym:",tickerSym # ticker is GRT-UN-T
        showMessage66(runScripts,"Fudged a BLANK Action")
                         # So far this is always a ROC(Return of Capital) from Granite GRT.UN
        time.sleep (10)  # need some time to display the message


    if action == 'Cash in lieu' :  # showed up $7.58 on M&B TNT when it split 1 for 5.75
        memo = memo + action
        action = 'Dividend'

    if action == 'Exchange' :  # this was on two MID436 transactions .. no idea what it means
        action = 'Dividend'

    if action == 'Dividend' and rate != 0 and val != None and amt != None  :  # MID436 transaction .. has Price(rate) and number of Stocks(val) and total amount(amt)
        print "277 We got a dividend reinvestment transaction for:",desc
        action = 'DVF' # dividend reinvest

    if  action.count ('Transfer in') > 0:  # cash from some where
        memo = memo + action
        action = 'BANK' # this worked ok but the transfer account is missing .. just uses "unknown" .. shows up in the Bank Register :)

    if  action.count ('RRIF transfer') > 0:  # cash or stocks from some where
        memo = memo + action
        if val != 0: # has stocks
          action = 'Buy'
        else:
          action = 'BANK'

    if  action.count ('Disbursement') > 0:  # free stocks from some where
        memo = memo + action
        if val != 0: # has stocks
          action = 'Buy'
        else:
          action = 'BANK'


    if  action.count ('Contribution') > 0:  # cash from some where
        memo = memo + action
        action = 'BANK' # this worked ok but the transfer account is missing .. just uses "unknown" .. shows up in the Bank Register :)

    if  action.count ('Payment') > 0:
        memo = memo + action
        action = 'BANK'
        XferCategory = "LIF Pension"

    if  action.count ('Federal tax') > 0:
        memo = memo + action
        action = 'BANK'
        XferCategory = "Tax:Income Tax"

    if  action.count ('De-registration fee') > 0:
        memo = memo + action
        action = 'BANK'
        XferCategory = "Bank Fees"

    if  action.count ('Withdrawal') > 0: # XferCategory could be Rita Pension, M&B Pension ,  TFSA Pension etc....
        memo = memo + action
        action = 'BANK'
        XferCategory = "M&B Pension"

    if  action.count ('Goods & Services Tax') > 0:
        memo = memo + action
        action = 'BANK'
        XferCategory = "Tax:GST"

    if  action.count ('RSP fee paid') > 0:
        memo = memo + action
        action = 'BANK'
        XferCategory = "Bank Fees"

    if  action.count ('Reinvestment') > 0:  # cash or stocks from some where like a DRIP
        memo = memo + action
        if val != 0: # has stocks
          action = 'Buy'
        else:
          action = 'BANK'

    if action == 'Interest'or action == 'Dividend': # negative dividends are a problem
      if amt < 0:
        print "342 processTxn Interest/Dividend amount is negative", amt/100.0 #moneydance dosn't handle negative dividends properly .. need to switch to MiscExp
        print "343 switching it to MiscExp" #Granite and Brookfield uses negative Interest dividends to correct errors
        action = 'MiscExp'



#    print '372 BUY/SELL amt=',amt
#    print '373 BUY/SELL val=',val
#    print '374 BUY/SELL rate=',rate
#    print '375 BUY/SELL BrokerFee =',BrokerFee

    AcctBook = rootAcct.getBook()                  #2015-1
    txnSet = AcctBook.getTransactionSet()          #2015-2 
    Partxn = ParentTxn.makeParentTxn(AcctBook,dateInt, dateInt, dateInt, "", invAcct,  desc, memo, -1, AbstractTxn.STATUS_UNRECONCILED) #2015
    if action == 'Buy' or action == 'Sell' or action == 'Redemption':                       # don't need an inc split because it doesn't effect your income
#      print 'BUY/SELL amt=',amt # 15000 = $150.00 total value of transaction (long ) 2 decimals
#      print 'BUY/SELL val=',val # 1000000 =  100 number of stocks (long ) 4 decimals # Quantity
#      print 'BUY/SELL rate=',rate # price 840.0 = $8.40  (float)  2 decimals         # Price
#      print 'BUY/SELL BrokerFee =',BrokerFee # fee 840.0 = $8.40 (float) 2 decimals
##      if secAcct == None: # already handled
##	print "Missing Security Account skiping txn"
##	return
      if action == 'Sell' or action == 'Redemption':
	 TxnUtil.setInvstTxnType(Partxn,InvestTxnType.SELL) # below needs to be tested on a BMO SELL
         secSplit = SplitTxn.makeSplitTxn(Partxn, long (amt - BrokerFee) , long(val* -1.0), rate , secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #SELL
#         secSplit = SplitTxn.makeSplitTxn(Partxn, long ((amt + BrokerFee) * -1.0 ), long(val* -1.0), rate , secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #SELL
      else:
	 TxnUtil.setInvstTxnType(Partxn,InvestTxnType.BUY) # BMO BUY amt is negative   #stocks   Price
         secSplit = SplitTxn.makeSplitTxn(Partxn, long ((amt + BrokerFee )* -1.0 ), long(val), rate, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)           #BUY
#         secSplit = SplitTxn.makeSplitTxn(Partxn, long (amt - BrokerFee ), long(val), rate, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)           #BUY
      TxnUtil.setSecurityPart(secSplit)
      Partxn.addSplit(secSplit)
      feeAcct = None  
      feeAcct = rootAcct.getAccountByName('Fees Broker')
      if feeAcct is None:
        print "377 no catagory Fees Broker"
        return     
      feeSplit = SplitTxn.makeSplitTxn(Partxn, long (BrokerFee) ,0,0, feeAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #fees
      TxnUtil.setCommissionPart(feeSplit)
      Partxn.addSplit(feeSplit)      
    elif action == 'BuyXfr' or action == 'SellXfr':
      return #........................................... not doing anything for Xfr buys and sells ... just use BANK and Buy/Sell
      if action == 'SellXfr':
	 TxnUtil.setInvstTxnType(Partxn,InvestTxnType.SELL_XFER)
         secSplit = SplitTxn.makeSplitTxn(Partxn, long ((amt + BrokerFee) * -1.0 ), long(val* -1.0), rate , secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #SELLXfr
      else:
	 TxnUtil.setInvstTxnType(Partxn,InvestTxnType.BUY_XFER)
         secSplit = SplitTxn.makeSplitTxn(Partxn, long (amt - BrokerFee ) , long(val), rate, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)               #BUYXfr   
      TxnUtil.setSecurityPart(secSplit)
      Partxn.addSplit(secSplit)
      feeAcct = None  
      feeAcct = rootAcct.getAccountByName('Fees Broker')
      if feeAcct is None:
        print "395 no catagory called Fees Broker"
        return     
      feeSplit = SplitTxn.makeSplitTxn(Partxn, long (BrokerFee) ,0,0, feeAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #fees
      TxnUtil.setCommissionPart(feeSplit)
      Partxn.addSplit(feeSplit)
      xfrAcct = None  
      xfrAcct = rootAcct.getAccountByName('BMO Chequing 3465')
      if xfrAcct is None:
        print "403 no transfer account called BMO Chequing 3465"
        return  
      if action == 'SellXfr':
	xfrSplit = SplitTxn.makeSplitTxn(Partxn,long (amt),long (amt),100.0, xfrAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #Selltransfer
      else:	
	xfrSplit = SplitTxn.makeSplitTxn(Partxn,long (amt * -1.0 ),long (amt * -1.0 ),100.0, xfrAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #Buytransfer
      TxnUtil.setXfrPart(xfrSplit)
      Partxn.addSplit(xfrSplit)
#    elif action == 'CASH DIV' or action == 'STOCKDIV':
    elif action == 'Dividend': # BMO also provides the number of shares which is not used
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.DIVIDEND)
      secSplit = SplitTxn.makeSplitTxn(Partxn, 0, 0, 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED) #2015 secAcct is for the ticker symbol stats
      TxnUtil.setSecurityPart(secSplit)
      Partxn.addSplit(secSplit)
      autoAcct = None  
      autoAcct = rootAcct.getAccountByName('non taxable dividend') # looks up an income catagory
      if autoAcct is None:
        print "420 no catagory called non taxable dividend"
        return
      incSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED) #autoAcct is the income catagory
      TxnUtil.setIncomePart(incSplit)
      Partxn.addSplit(incSplit)

      feeAcct = rootAcct.getAccountByName('Fees Broker')
      if feeAcct is None: print "449 Error no catagory Fees Broker"; return
      feeSplit = SplitTxn.makeSplitTxn(Partxn, long (BrokerFee) ,0,0, feeAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #fees
      TxnUtil.setCommissionPart(feeSplit)
      Partxn.addSplit(feeSplit)

#   see moneydance-API-doc.ods in Lessons/moneydance/Investment-Accounts
# A DivReinvest has 3 splits 1-security secSplit 2-incSplit or expSplit(shows as Category) 3-optional Fee Category .. feeSplit
    elif action == 'DVF': # dividend reinvestment .. has stocks(val) .. Price(rate)(optional) and total amount(amt) , no fees  ..
# the Price(rate) gets changed by moneydance to keep the amt(cash) and val(shares) as specified
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.DIVIDEND_REINVEST)
#      TypeError: makeSplitTxn(): 3rd arg can't be coerced to long ... val
#      secSplit = SplitTxn.makeSplitTxn(Partxn, 0, val, 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)
                                             # amt=total cost , val=stocks , rate=stock price , fee=?
                                             # there is no BrokerFee on a DVF .. seemed to fix the middleton round off error
#      secSplit = SplitTxn.makeSplitTxn(Partxn, long(amt - BrokerFee), long(val), rate, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)     # borrowed from Buy
      secSplit = SplitTxn.makeSplitTxn(Partxn, long(amt), long(val), rate, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED) # removed the BrokerFee
#      secSplit = SplitTxn.makeSplitTxn(Partxn, long(amt), long(val), 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)   # this works too .don't really need the Price
      TxnUtil.setSecurityPart(secSplit)
      Partxn.addSplit(secSplit)
# need to set the income category so account balance doesn't get messed up
      autoAcct = None
      autoAcct = rootAcct.getAccountByName('non taxable stock dividend') # looks up the income catagory
      if autoAcct is None:
        print "450 DVF no catagory called 'non taxable stock dividend'"
        return
      incSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED) #2015 autoAcct is the income catagory like "Dividend Income"
      TxnUtil.setIncomePart(incSplit)
      Partxn.addSplit(incSplit)
# there are no Fees on a DVF .. the feeSplit account will default to 'unknown'
#      feeAcct = rootAcct.getAccountByName('Fees Broker')
#      if feeAcct is None: print "Error 514 no catagory Fees Broker"; return
#      feeSplit = SplitTxn.makeSplitTxn(Partxn, long (BrokerFee) ,0,0, feeAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #fees
#      TxnUtil.setCommissionPart(feeSplit)
#      Partxn.addSplit(feeSplit)

    elif action == 'MiscInc':    # we could have no security to go with this income maybe just interest on cash in the account
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.MISCINC)
      if secAcct != None:    # must have found a ticker
         secSplit = SplitTxn.makeSplitTxn(Partxn, 0, 0, 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)
         TxnUtil.setSecurityPart(secSplit)
         Partxn.addSplit(secSplit)
      autoAcct = None  
      autoAcct = rootAcct.getAccountByName('non taxable interest') # a catagory
      if autoAcct is None:
        print "471 no catagory called non taxable interest"
        return
      incSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED)
      TxnUtil.setIncomePart(incSplit)     
      Partxn.addSplit(incSplit)

      feeAcct = rootAcct.getAccountByName('Fees Broker')
      if feeAcct is None: print "500 Error no catagory Fees Broker"; return
      feeSplit = SplitTxn.makeSplitTxn(Partxn, long (BrokerFee) ,0,0, feeAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #fees
      TxnUtil.setCommissionPart(feeSplit)
      Partxn.addSplit(feeSplit)

    elif action == 'Interest': # BMO also provides the number of shares which is not used
#      print "508 processTxn changing Interest to Dividend" # moneydance has no such thing as Interest everything is a dividend (taxable or not taxable ?)
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.DIVIDEND)
      if secAcct != None:    # must have found a ticker
         secSplit = SplitTxn.makeSplitTxn(Partxn, 0, 0, 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)
         TxnUtil.setSecurityPart(secSplit)
         Partxn.addSplit(secSplit)
#      autoAcct = None
#      autoAcct = rootAcct.getAccountByName('non taxable interest') # a catagory
      autoAcct = rootAcct.getAccountByName('Interest Income') # Interest is taxable
      if autoAcct is None:
        print "494 no catagory called Interest Income"
        return
      incSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED)
      TxnUtil.setIncomePart(incSplit)     
      Partxn.addSplit(incSplit)

      feeAcct = rootAcct.getAccountByName('Fees Broker')
      if feeAcct is None: print "523 Error no catagory Fees Broker"; return
      feeSplit = SplitTxn.makeSplitTxn(Partxn, long (BrokerFee) ,0,0, feeAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #fees
      TxnUtil.setCommissionPart(feeSplit)
      Partxn.addSplit(feeSplit)

    elif action == 'MiscExp':    # we could have no security to go with this expense maybe just more bank fees. the amt sign needs to be negitive in the csv file
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.MISCEXP)
      if secAcct != None:    # must have found a ticker
         secSplit = SplitTxn.makeSplitTxn(Partxn, 0, 0, 0, secAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)
         TxnUtil.setSecurityPart(secSplit)
         Partxn.addSplit(secSplit)
      autoAcct = None  
      autoAcct = rootAcct.getAccountByName('unknown') # a catagory
      if autoAcct is None:
        print "515 no catagory called unknown"
        return
      expSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED)
      TxnUtil.setExpensePart(expSplit)     
      Partxn.addSplit(expSplit)

      feeAcct = rootAcct.getAccountByName('Fees Broker')
      if feeAcct is None: print "544 Error no catagory Fees Broker"; return
      feeSplit = SplitTxn.makeSplitTxn(Partxn, long (BrokerFee) ,0,0, feeAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #fees
      TxnUtil.setCommissionPart(feeSplit)
      Partxn.addSplit(feeSplit)

    elif action == 'BANK' :
      TxnUtil.setInvstTxnType(Partxn,InvestTxnType.BANK)
#      print"570 BANK XferCategory",XferCategory
#      autoAcct = rootAcct.getAccountByName('unknown') # a catagory.
      autoAcct = rootAcct.getAccountByName(XferCategory)
###      autoAcct = rootAcct.getAccountByName('non taxable dividend')
      if autoAcct is None: print "533 no catagory called ", XferCategory
###        return

#####      incSplit = SplitTxn.makeSplitTxn(Partxn, -amt, -amt, 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED)
#####      Partxn.addSplit(incSplit)  # no income on a BANK transfer
####
      xfrSplit = SplitTxn.makeSplitTxn(Partxn, -long(amt), -long(amt), 0, autoAcct, '', -1, AbstractTxn.STATUS_UNRECONCILED)
      TxnUtil.setXfrPart(xfrSplit)
      Partxn.addSplit(xfrSplit)       # fills in the "Transfer" account name with "Bank Fees" etc..
#      print "539 amt BrokerFee",amt,BrokerFee
####      feeAcct = rootAcct.getAccountByName('Fees Broker')  # no Broker Fees on a BANK tranfer
####      if feeAcct is None: print "Error 514 no catagory Fees Broker"; return
####      feeSplit = SplitTxn.makeSplitTxn(Partxn, long (BrokerFee) ,0,0, feeAcct, desc, -1, AbstractTxn.STATUS_UNRECONCILED)  #fees
####      TxnUtil.setCommissionPart(feeSplit)
####      Partxn.addSplit(feeSplit)
    else: 
      print "549 Error Unknown action", action # this is a big deal you will need to edit this script
      print "550 Desc ",desc
      print "551 secAcct ",secAcct
      showMessage66(runScripts,"Unknown Action Faking a Dividend ")
      memo = 'Fake ' + memo
      time.sleep (10)  # need some time to display the message
      processTxn(rootAcct, invAcct, secAcct, dateInt, desc, memo,'Dividend', amt, val, rate, BrokerFee, tickerSym) # try recursion
#      raise Exception ('Unknown Action',action)
      return
    txnSet.addNewTxn(Partxn)
    time.sleep (0.100)  # seems to have fixed the thread crashs ... its in seconds ,,,, 100 milliseconds
#.........................................end of processTxn function    
    
  print "562 BMO-Inv-new.py reading transactions from ",csvfile
  accountName = None
  while(1):
    if len(sys.argv) < 3:
      print '566 this script needs 3 arguments to run'
      break
    if len(sys.argv[1]) < 6:
      print '569 this script needs argv[1] filled in with runScripts'
      break
    if len(sys.argv[2]) < 6:
      print '572 this script needs argv[2] filled in with the Account Name'
      break
    if sys.argv[1] != 'runScripts':
      print '575 argv[1] must be runScripts'
      break
    print "577 accountName ",sys.argv[2]
    accountName = sys.argv[2]
#    print sys.argv[1] 
#    print sys.argv[2]
    sys.argv = [''] # clean the arguments out.
    break  
  
  if accountName == None:
      print "585 We need an Account Number"
      raise Exception ('We need an Account Number')

#  raise Exception('I know Python!')
# .........................................................Script begins execution here
  
  root = moneydance.getRootAccount()
  #currencies = root.getCurrencyTable()

#  fin = open( runScripts.infile ,'r') # this is the csv file we are going to process
  fin = open( csvfile ,'r') # this is the csv file we are going to process

  sym = fin.readline()                 #read the first line and throw it away
  print "598 HEADER",sym
  sym = fin.readline()                 #read the second line and throw it away
  sym = fin.readline()                 #read the third line and throw it away



  while 1:
    sym = fin.readline()
    if len(sym) <= 0:
      break
#  sym = sym.replace(',',' ') # don't change , to blanks
    lst = sym.split(',')
    print"610 lst", lst
    
# Note BMO has hidden the fee in the "Total Amount" and moneydance adjusts the price to compensate. Messes things up
# so the amt passed to moneydance needs to be "Total Amount" + Fee and the Fee needs to be calculated and updated
# moneydance displays the amt - the fee so if you add the fee to it on a "SELL" it works out. On a "Buy" it should be the opposite.
# the amt passed to moneydance needs to be the result of the sale or purchase without the fee.
# "Fees Broker" is a good category/Account for the fees
# sample of the BMO investor line csv file layout.Note that the symbol is missing on one transaction . also the account #
#Transaction Type=All	Product Type=All	Period=	From=2017-12-01	To=2018-03-15
# note that the memo field is missing from the csv file .. it shows in the statement with like 4 lines of text in the Desc field .. where did it go ?
# The desc seems to be just the first line.
#Transaction Date	Settlement Date	Activity Description	Description	              Symbol	Quantity	Price	Currency	Total Amount	Currency
#----------------	---------------	--------------------	-----------	              ------	--------	-----	--------	------------	--------
#2018-03-01     	2018-03-01	      Dividend	        CDN UTIL 4.5% CUM RDM SECND PR	CU.PR.F	  700		                          196.88	CAD
#2018-01-15	        2018-01-17	        Buy	        EXCHANGE INC CORP	         EIF	  400	         33.25	    CDN	        -13309.95	CAD
#2018-01-15	        2018-01-15	      Interest	        REIT INDEXPLUS INC FD TR UNITS	IDR.UN	  1000			                      65	CAD
#2017-12-14	        2017-12-14	      Redemption	1000THS CANOE CDN ASSET ALLOC		  -862			                       0        CAD
#2017-12-12	        2017-12-14	        Sell	        CANOE CDN ASSET ALLOC CL SR Z(	GOC309	 -5529	          9.436	     CDN	  52179.78	CAD
# sample of the Scotia csv file layout.
#Description	                                                                                Symbol	Transaction Date	Settlement Date	Account Currency	Type	Quantity	Currency of Price	Price	Settlement Amount
#PATHFINDER INCOME FUND TR UNIT DIST      ON    1000 SHS REC 01/31/18 PAY 02/15/18      	PCD.UN	15-Feb-2018	        15-Feb-2018     	  CAD	      CASH DIV	   0	          CAD	                   0	    50


#    print 'Tranaction Date=',lst[0]
#    print 'Settlement Date=',lst[1]
#    print '552 Activity=',lst[2]
#    print 'Description=',lst[3]
#    print 'Symbol=',lst[4]
#    print 'Quantity=',lst[5]
#    print 'Price=',lst[6]
#    print 'Currency of Price=',lst[7]
#    print 'Total Amount=',lst[8]
#    print 'Currenty of Amount =',lst[9]
    
#  dateInt = mdDate(row['Date'])

# ..........................................................  Date
    transdate = lst[0].split('-')
    day = transdate[2]
    month = transdate[1]
    year= transdate[0]
#    print 'day=',day
#    print 'month=',month
#    print 'year=',year

    date = str2dateBMO ( day,month,year )
    transdate = int (strftime("%Y%m%d",date)) # 20120130
#    print transdate

#    invAcct = root.getAccountByName(runScripts.accountName)
    invAcct = root.getAccountByName(accountName)
    if invAcct is None:
      print "662 BMO-Inv-new.py missing the name of the Moneydance Investment account to update"
      print "663 accountName=", accountName
      break
# fill in the memo field with something useful since its missing in the csv file
# all subsequent memo entries should be memo = memo + "something"
# its used as a way to communicate with the user of this script

#    memo = 'BMO-Inv-new.py'
    import datetime

    t = datetime.datetime.now()
    memo = t.strftime('%m/%d/%Y-%I-%M-%S ')

#    print ("720 memo",memo)
#    print (x)
#    print(x.year)
#    print(x.month)
#    print(x.day)
#    print(x.hour)
#    print(x.minute)
#    print(x.second)

#    raise Exception ('Testing')
    
    secAcct = None  
# ...........................................................tickerSym
    tickerSym = lst[4]
#    print "tickerSym 703 len,Sym",len(tickerSym),tickerSym # for some reason len is 1 .. its a space
#    if (tickerSym == ' '):
#      print "tickerSym is a blank"

    if (len(tickerSym) <= 0) | (tickerSym == ' '): 
      tickerSym = None
##      print "Missing ticker symbol, trying to Look it up using its description "
##      tickerSym = None
##      Description = lst[3]
##      Description = Description[:10] #20 was too long try 10 characters
##      print "DESC=", Description
##      for fundsym , fundname in DescTable.items():
###        print fundsym , fundname
###        print len(fundname)
##	if len(fundname) <= 0: break
##	if  fundname.count (Description) > 0:
##	  print "found it", fundsym ,fundname
##	  tickerSym = fundsym
##	  memo = 'Ticker Found'
###	print "found tickerSym=",tickerSym
##	  break
##      if tickerSym == None:
##        print "Ticker symbol Look up failed ------------------------.  TXN"
    else: # we got a good one
      tickerSym = tickerSym.replace('.','-') 
      tickerSym = tickerSym+"-T" #  what about the other stock exchanges
      for tsxSym ,NYXSym in definitions.SymbolTable.items():  #check to see if this symbol is on a different stock exchange then the TSX
#        print tsxSym , NYXSym
#        print len(NYXSym)
	if len(NYXSym) <= 0: break
	if  tsxSym == tickerSym:
	  print "720 Not on TSX", tsxSym ,NYXSym
	  tickerSym = NYXSym
#          print "new tickerSym=",tickerSym
	  break

      
#    print 'ticker ',tickerSym #prints SIS-T

    if tickerSym != None:  
      secAcct = getSecurityAcct(root, invAcct, tickerSym)
      if secAcct is None:
         print "731 This security needs to be added to the account"
         print "732 Using Fake-T  for now"
         secAcct = getSecurityAcct(root,invAcct,"FAKE-T") # just fake it
         if secAcct == None:
	   raise Exception ('Security FAKE-T is missing, add it to your account')
         memo = memo + 'Ticker Not found'
#      if secAcct is None: # the ticker we have is no good .. lookupTicker is missing in BMO but exists in Scotia
#	tickerSym = lookupTicker(Description,DescTable) # maybe its the wrong ticker on the record see if we can find the right one.
#	secAcct = getSecurityAcct(root, invAcct, tickerSym)
#        if secAcct is None: # the ticker is still no good
#          secAcct = getSecurityAcct(root,invAcct,"FAKE-T") # just fake it
#          if secAcct == None:
#	     raise Exception ('FAKE-T missing')
#          memo = 'BAD Ticker'
#	  print "BAD Ticker getSecurityAcct Failed for",tickerSym
    else: # ticker is None
#      print "This transaction has no tickerSymbol guessing"
#      secAcct = invAcct.getSubAccount(0) # fake it  
      secAcct = getSecurityAcct(root,invAcct,"FAKE-T") # just fake it  
      if secAcct == None:
	raise Exception ('Security FAKE-T is missing')
      memo = memo + 'Ticker Missing'
  
#.........................................Quantity.......................................................................
    decimals = secAcct.getCurrencyType().getDecimalPlaces() # securities (stocks) are stored with 4 decimal places
#    userRate = secAcct.getCurrencyType().getUserRate()
#    print '759 decimals used for Stock Quantity' ,decimals
    if decimals != 4 and decimals != 5:
      print '759 decimals are:', decimals
      raise Exception ('764 Decimals must be 4 or 5')
#    print 'UserRate used for Stock Quantity' ,userRate
    if decimals == 4:
      Quantity = mdQty(lst[5], 4 )  # in csv file, buy is > 0, sell is < 0  #number of stocks , BMO may have 4 decimal places (mutual funds)

    if decimals == 5:
      Quantity = mdQty(lst[5], 5 )

    if Quantity < 0:
      Quantity = Quantity * (-1.0)      # let the BUY / SELL action decide on the + or - sign

#    print '780 Quantity decimals',Quantity , decimals

#...................................Price .......................................................................................................................
    Price = mdQty(lst[6], 4 )  # the price could have up to 4 decimal places in the csv .. the csv file has 11.3883 in it ... only middlefield has 4 places
#    print '784 Price', Price   # 113883  .. moneydance uses doubles for price
    PriceRaw = Price / 100.0   # money dance only uses 2 decimal places on price so drop 2 places and convert to float
#    print '786 PriceRaw', PriceRaw   # 1138.83   .. this shows the round off error .83 will be dropped BMO uses 4 decimal places on price.
#    print '787 % the fraction ', Price % 1   # just the fraction .83
#    print '788 // the integer ', Price // 1   # the integer 1138
    if (PriceRaw % 1 ) != 0 :
       print '785 BMO is using more than 2 decimals on Price'
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
       print '795 BMO is using more than 2 decimals on Amount(dollars)'

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
    

#   processTxn(rootAcct, invAcct,    secAcct, dateInt,    desc,  memo, action, amt,     val,      rate  , BrokerFee):  
    processTxn(root,     invAcct ,   secAcct, transdate ,lst[3], memo, lst[2], Amount,  Quantity, Price , BrokerFee , tickerSym )
#    raise Exception('I know Python!')    
 
#######  root.refreshAccountBalances()  #not in 2015

  AcctBook = root.getBook() 
  AcctBook.refreshAccountBalances()
  print "847 Done BMO-Inv-new.py"
#................................................................................script execution ends here
