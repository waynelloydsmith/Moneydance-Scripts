# Moneydance-stockglance75.py
This jython script is run by using the monydance->Window->"Show MoneyBot Console"
Then "Open Script" pick stockglance75.py then pick "run".
The enhancment StockGlance75 has over StockGlance is that it shows you which
accounts your investments are held in. It is not easy to find this out in moneydance.
Some times the same security is held in multiple accounts.
The script should be placed in /opt/moneydance/scripts.
You may need to create the /opt/moneydance/scripts directory and add 
....................................................................
import os
os.chdir('/opt/moneydance/scripts')
import sys
sys.path.append(r'/opt/moneydance/scripts/')
....................................................................
to the stockglance75.py script file or use another startup script to set these up .
Yoy also need to update the days prices with updateDaylyStockwarch.py or it may crash.

