#!/usr/bin/env Jython
# coding: utf8
# called by updateDaylyStockwatch.py (which uses execfile)



import sys
import urllib2
import urllib

#raise Exception('I know Python!')


file2 = open('/opt/moneydance/scripts/tmp/StockwatchDay/stockwatch.csv', 'wb')
print file2

#url =  'http://www.stockwatch.com/Quote/Download.aspx?type=date&format=ascii&dest=file&date=20171222&exopt=N&ex=T&ats=N&id=username&pw=password' # end of day closing
#url = 'http://www.stockwatch.com/Quote/WebQuery.aspx?what=quote&format=comma&fields=SXRLVOHITE&pf=1&region=C&header=Y&id=username&pw=password' # my portfolio worked

#&ex=TE   gets both NEO and the TSX
#&ats=Y   includes volumes from the ATS exchanges
#&exopt=N ???  I changed this to Y and didnt see any difference in the files
#Exchange	# Data Point
#B - CBOE Indexes	301	american indexes
#C - CSE	        215	Canadian Securities Exchange 
#D - CanDeal	        649	Canadian Bonds
#E - AQ-NEO	         31	
#F - CA Mutual Funds	7062	
#I - Indexes	        4830 has exchanges rates in it.	
#Q - Nasdaq	        8740	
#S - S&P Indexes	2482	
#T - TSX	        1892	
#V - TSX-V	        1320	
#X - Amex	        2020	
#Z - NYSE	        3101	
#M - Montreal	        2845	was empty 
#O - OPRA	       121469   options
# so currently there is no mutual fund prices in the download file. I don't have any  ..need &ex=TEVF for this...

userName = 'your-user-name'
password = 'your-password'
#print 'Username',userName
#print 'password',password
#raise Exception('I know Python!')

url = 'https://www.stockwatch.com/Quote/Download.aspx?type=date&format=ascii&dest=file&exopt=N&ex=TEV&ats=Y&id=' + userName + '&pw=' + password
# most recent end of day closing prices .. no date .. returns an empty file if the markets are closed

print '57 url ' , url
#raise Exception('I know Python!')

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0 SeaMonkey/2.49.1 Slackware/14.2')]

req = urllib2.Request(url)
try:
  response = opener.open(url)
except urllib2.URLError as e:
    if hasattr(e, 'reason'):
        print '68 We failed to reach a server.'
        print '69 Reason: ', e.reason
    if hasattr(e, 'code'):
        print '71 The server couldn\'t fulfill the request.'
        print '72 Error code: ', e.code
else:  
  print '74 response ', response.headers
  webContent = response.read()           # just got a single line of column headings when the market was closed.for days close request
  print '76 length=', len(webContent)       #  got  1932 lines when I specified a day
#  print webContent


  file2.write(webContent) # this function does not return anything useful ..
# I changed the permission on the file and crashed the program with an IOError:[Errno 13] Permission denied:  
  file2.close() 
  print "83 Done fetchhtmlDaylyStockwatch.py"
#  raise Exception('I know Python!')


