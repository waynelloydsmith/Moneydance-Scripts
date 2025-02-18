These scripts are used by me almost dayly to keep my moneydance Investment accounts up to date.
runScripts.py is a Jython Java swing program that allows you too quicly choose which script you want to run.
I put dummy Accounts in AccountNames.py
The account numbers must match what ever your using in moneydance.
You need to put your stockwatch user name and password in Passwords.py
You only need a Stockwatch account if you want to run UpdateDaylyStockwatch.py
you run it at the end of the trading day to get the close prices put into moneydance
updateHistoryStockwatch.py will load a years worth of price history into moneydance for a ticker.
You have to manualy download the history files from stockwatch to do this first.
Put all the scripts in /opt/moneydance/scripts
Then you could run execfile("runScripts.py") on a jython console.
or use the moneydance Developer Console to Open the Script and then Run it.
The Investment Account tranaaction update scripts assume you have downloaded
the csv files from the bank and put them in ~/Downloads
runScripts runs BMO-Inv-new.py 
Scotia-Inv-new.py can be run from a console or the moneydance developer console.

