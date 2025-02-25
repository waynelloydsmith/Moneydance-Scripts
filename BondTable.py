#!/usr/bin/env python
# coding: utf8
# version 2/19/2025

global BondTable
BondTable = dict({ # a dictionary of dictionaries
#    '5VJYFL0':{'desc':'ZAG BANK MONTHLY INTEREST GIC','coupon':2.95,'date':'2023-03-15','accrued':0,'fee':0},
    '5VJYFL0'  :{'desc':'DESJARDINS TRUST INC MONTHLY INTEREST GIC','coupon':2.95,'date':'2023-03-15','accrued':0,'fee':0},
    '13321LAH1':{'desc':'CAMECO CORPORATION','coupon':3.75,'date':'2022-11-14','accrued':246.58,'fee':24.99},
    '136765BA1':{'desc':'CANADIAN WESTERN BANK SR UNSECURED','coupon':2.924,'date':'2022-12-15','accrued':142.60,'fee':24.99},
    '11257ZAC3':{'desc':'BROOKFIELD ASSET MGMT INC MED TERM NTS','coupon':4.54,'date':'2023-03-31','accrued':410.47,'fee':24.99},
    '303901AZ5':{'desc':'FAIRFAX FINANCIAL HLDS LTD SR UNSECURED','coupon':4.25,'date':'2027-12-06','accrued':232.88,'fee':24.99},
    '51925DBP0':{'desc':'LAURENTIAN BANK OF CANADA SENIOR DEPOSIT NOTES','coupon':3.0,'date':'2022-09-12','accrued':3.29,'fee':24.99},
    '5W62553'  :{'desc':'BANK OF MONTREAL ANNUAL INTEREST GIC DUE 11/15/2024  INT  2.350% CPN' },
    '5K01225'  :{'desc':'BANK OF NOVA SCOTIA (THE) ANNUAL INTEREST GIC DUE 07/07/2025  INT  5.050% CPN INT   ON    4500 BND REC 07/04/24 PAY 07/05/24' }
    })

# don't forget the comma on the line above the one you just entered at the bottom of the list
#  Accrued interest is the amount of interest earned on a debt, such as a bond, but not yet collected.
# so when you buy it you have to pay the seller the amount Accrued on the bond because the date you buy it doesn't match the date it pays on.
# the date field is the date the bond will be redeemed ,
# what is missing in this table is the payment frequency .. maybe annual , semi-annual , quarterly or monthly
# also what Bank is holding it for you .. Scotia iTrade or BMO Investor line
# this frequency changes the Accrued amount
