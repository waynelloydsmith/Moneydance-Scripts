#!/usr/bin/env python
# coding: utf8
# version March/2/2025

# used by lookupTicker() in Scotia-Inv-new.py
# these descriptions must match what Scotia iTrade uses ... not what moneydance uses.. or stockwatch uses
# some mutual funds are in this table but are not used any more. note that they don't carry the -T because they do not trade on the TSX'
# a python dictionary ... a dictionary of lists works better see BMOdescTable.py
global ScotiaDescTable
ScotiaDescTable = {
   'TML202':'FRANKLIN BISSETT CDN EQUITY FD (202)',
   'MFC738':'CUNDILL CANADIAN SECURITY FUND SER C (738)',
   'BIP151':'BRANDES GLOBAL EQUITY FUND (151)',
   'FID281':'FIDELITY CANADIAN ASSET ALLOCATION FUND ISC (281)',
   'BNS344':'SCOTIA SELECTED MAXIMUM GROWTH PORTFOLIO (344)',
   'BNS361':'SCOTIA MORTGAGE INCOME FUND (361)',
   'BNS741':'SCOTIA SELECTED BALANCED INCOME & GROWTH PORTFOLIO (741)',
   'BNS357':'SCOTIA MONEY MARKET FUND (357)',
   'BMO146':'BMO DIVIDEND FUND (146)',
   'BMO471':'BMO Select Trust Fixed Income (471)',
   'GOC309':'CANOE CANADIAN ASSET ALLOCATION CLASS SERIES Z(309)',
   'AI-T':'Atrium Mortgage Investment Corporation',
   'ARX-T':'ARC RESOURCES LTD',
   'ABX-T':'BARRICK GOLD',
   'AD-T':'ALARIS ROYALTY CORP',
   'ALA-T':'ALTAGAS LTD',
   'APR-UN-T':'AUTOMOTIVE PROPERTIES RL EST INVEST TRUST (2015)',
   'AW-UN-T':'A&W Revenue Royalties Income Fund',
   'AX-UN-T':'Artis Real Estate Investment Trust',
   'BR-T':'BIG ROCK BREWERY INC',
   'BTB-UN-T':'BTB REAL ESTATE INVESTMENT TRUST',
   'BNE-T':'BONTERRA ENERGY CORP',
   'BPF-UN-T':'BOSTON PIZZA ROYALTIES INCOME FUND TRUST',
   'CCO-T':'CAMECO CORP',
   'CRR-UN-T':'Crombie Real Estate Investment Trust',
   'CNR-T':'CANADIAN NATIONAL RAILWAY CO',
   'CTF-UN-T':'CITADEL INCOME FUND',
   'CIQ-UN-T':'CANADIAN HIGH INCOME EQUITY FUND',
   'CJR-B-T':'CORUS ENTERTAINMENT INC',
   'CU-PR-F-T':'CDN UTIL 4.5% CUM RDM SECND PR',
   'DS-T':'Quadravest Dividend Select 15 Canadian', # Quadvest
   'DR-T':'MEDICAL FACILITIES CORPORATION',
   'EIT-UN-T':'CANOE EIT INCOME FD',
   'EIF-T':'EXCHANGE INC CORP',
   'ENF-T':'ENBRIDGE INCOME FD HLDGS',
   'EXE-T':'Extendicare Inc',
   'FTS-T':'FORTIS INC',
   'FC-T':'FIRM CAPITAL MORTGAGE INV. CORP',
   'FCD-UN-X':'Firm Capital Property Trust',           # its on the TSX venture exchange ?
   'FFN-PR-A-T':'Quadravest North American Financial 15 Split Corp',
   'FFI-UN-T':'FLAHERTY & CRUMRINE INVESTMENT',
   'FTN-PR-A-T':'Quadravest Financial 15 Split Corp US and Canada',
   'FN-T':'First National Financial Corp',
   'FIG-T':'First Asset Investment Grade Bond ETF',
   'GWO-PR-S-T':'GREAT-WEST LIFECO INC PR',
   'GDG-UN-T':'GLOBAL DIVIDEND GROWERS INCOME FUND',
   'G-T':'GOLDCORP INC',                               # goldcorp us dollars
   'HR-UN-T':'H&R REAL ESTATE INVESTMENT TRUST STAPLED',
   'H-T':'HYDRO ONE',
   'HHL-T':'HEALTHCARE LEADERS INCOME ETF',
   'IDR-UN-T':'REIT INDEXPLUS INC FD TR UNITS',
   'IDR-T':'MIDDLEFIELD REIT INDEXPLUS ETF UNIT',
   'IPL-T':'INTER PIPELINE LTD',
   'INC-UN-T':'INCOME FINANCIAL TRUST',
   'JE-T':'JUST ENERGY GROUP INC',
   'K-T':'KINROSS',
   'KMB-N':'KIMBERLY CLARK',                           # Kimberly Clark on New York Exchange
   'KEG-UN-T':'THE KEG ROYALTIES INCOME FUND',
   'KWH-UN-T':'CRIUS ENERGY TRUST',
   'LFE-PR-B-T':'Quadravest 4 Canada Life Companies Split Corp',
   'MFR-UN-T':'MANULIFE FLOATING RATE SR LN FD',
   'MFT-T':'Mackenzie Floating Rate Income ETF',
   'MHYB-NEO':'MACKENZIE GLBL HIGH YLD ETF',
   'MID-UN-T':'MINT INCOME FUND TR',
   'MUB-T':'Mackenzie Unconstrained Bond ETF',
   'MR-UN-T':'Melcor Real Estate Investment Trust',
   'MRT-UN-T':'MORGUARD REAL ESTATE INVESTMENT TRUST',
   'MMP-UN-T':'PRECIOUS METALS AND MINING TRUST',
   'NPF-UN-T':'NORTH AMERICAN PREFERRED SHARE FUND',
   'NWH-UN-T':'NORTHWEST HEALTHCARE PROPERTIES REIT',
   'OCV-UN-T':'YIELD ADVANTAGED CONV DEB FUNDS',
   'ONR-UN-T':'ONEREIT TR UNIT',
   'PEY-T':'Peyto Exploration & Development Corp',
   'PCD-UN-T':'MiddleField PATHFINDER INCOME FUND',
   'PGI-UN-T':'PIMCO GLOBAL INCOME OPPORTUNITIES FD',
   'PLZ-UN-T':'PLAZA RETAIL REIT TRUST',
   'PPL-T':'Pembina Pipeline Corporation',
   'PR-T':'LYSANDER-SLATER PREFERRED SHARE ACTIVE ETF',
   'PGF-T':'PENGROWTH ENERGY CORPORATION',
   'PKI-T':'PARKLAND FUEL CORPORATION', # was PKI.UN jan 7 2011
   'REI-UN-T':'RIOCAN REAL ESTATE INVESTMENT TRUST',
   'REF-UN-T':'CANADIAN REAL ESTATE INVESTMENT TRUST',
   'RIT-T':'First Asset Canadian REIT ETF',
   'RBN-UN-T':'Brompton BLUE RIBBON INCOME FUND TRUST',
   'SCW-UN-T':'Canso Select Opportunities Fund',
   'SIN-UN-T':'SCITI TRUST',
   'SJR-B-T':'SHAW COMMUNICATIONS INC. CL B',
   'SKG-UN-T':'SKYLON GROWTH & INCOME TRUST',
   'SPB-T':'SUPERIOR PLUS CORP',
   'S-T':'SHERRITT INTERNATIONAL CORP',
   'SRU-UN-T':'SMARTCENTRES RL EST INVEST TR',
   'SRV-UN-T':'SIR ROYALTY INCOME FUND',
   'SSF-UN-T':'Brompton SYM FLOATING RTE SENIOR LOAN FND',
   'SU-T':'SUNCORE',
   'TECK-A-T':'Teck Resources Limited Class A Multiple Voting Shares',
   'T-T':'TELUS',
   'TNT-UN-T':'TRUE NORTH COMMERCIAL RL EST INVEST TR',
   'TF-T':'Timber Creek Financial Corp',
   'TA-T':'TRANSALTA',
   'UTE-UN-T':'CDN UTIL & TELECOM INC FD TR U',
   'VET-T':'VERMILLION ENERGY INC CORP',
   'WJA-T':'WESTJET',
   'YP-UN-T':'YIELDPLUS INCOME FUND TRUST',                             # merged into MID.UN and delisted March 24 2017
   'ZWE-T':'BMO Europe High Dividend Covered Call Hedged to CAD ETF',
   'ZWU-T':'BMO Covered Call Utilities ETF'

   }


# some testing
#if 'WJA-T' is in ScotiaDescTable : print 'True' # doesn't work on a dictionary'
#SyntaxError: no viable alternative at input 'in'
###if 'WJA-T' in ScotiaDescTable : print 'True' # prints True
###else: print 'False'
# The below makes the lookup function unnecessary
#if 'WESTJET' in ScotiaDescTable.values(): print 'True2' # printed True2
###if 'WESTJETTT' in ScotiaDescTable.values(): print 'True2' # printed False2
###else: print 'False2'
