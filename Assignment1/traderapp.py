#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 21:30:38 2017
This is the console based app for trading.
DATA602 Assignment 1

@author: dilipganesan
"""
import pandas as pd
import urllib.request
from collections import OrderedDict
from bs4 import BeautifulSoup
from datetime import datetime


"""
This is the function for Title Bar
"""

# Size of protfolio.
portfolioWorth = 10000000
# Blotter Data frames, which stores all transactions.
df2 = pd.DataFrame()
dfama = pd.DataFrame()
dfmicro = pd.DataFrame() 
dfintel = pd.DataFrame()
dfsnap = pd.DataFrame()
# This counter is used to order records in blotter based on transaction time.
ordercounter = 0


# Data Structure to hold Apple Values.
applelist=[]
applewap = 0.000
appleupl = 0
applerpl = 0
appleposition = 0
buyercounter = 0
buyerpricecounter = 0
sellcounter = 0
sellpricecounter = 0

# Data Structure to hold Amazon Values.
amazonlist=[]
amazonwap = 0.000
amazonupl = 0
amazonrpl = 0
amazonposition = 0
amazonbuyer = 0
amazonbuyprice = 0
amazonsellcounter = 0
amazonsellpricecounter = 0

# Data Structure to hold Microsoft Values.
microlist=[]
microwap = 0.000
microupl = 0
microrpl = 0
microposition = 0
microbuyer = 0
microbuyprice = 0
microsellcounter = 0
microsellpricecounter = 0

# Data Structure to hold Intel Values.
intellist=[]
intelwap = 0.000
intelupl = 0
intelrpl = 0
intelposition = 0
intelbuyer = 0
intelbuyprice = 0
intelsellcounter = 0
intelsellpricecounter = 0

# Data Structure to hold SNAP Values.
snaplist=[]
snapwap = 0.000
snapupl = 0
snaprpl = 0
snapposition = 0
snapbuyer = 0
snapbuyprice = 0
snapsellcounter = 0
snapsellpricecounter = 0


def get_title_app():
    print("\t**********************************************")
    print("\t***  Trader App Welcomes You!  ***")
    print("\t**********************************************")
    get_user_input()
    
     
"""
This is the 1st function for getting User Option, which trigger other functions.
"""
def get_user_input():
    print("\n[1] Trade")
    print("[2] Show Blotter")
    print("[3] Show P/L")
    print("[q] Quit")
    while True:
        try:
            user_option = input("What would you like to do? ")
            print("User Option-->"+user_option)
            if(user_option == "q"):
                input("Are you sure you want to Quit")
                print("\t**********************************************")
                print("\t***  Good Bye See you Soon!  ***")
                print("\t**********************************************")
                break
            elif(user_option == "1"):
                 doTrade()
            elif(user_option == "2"):
                showBlotter()
            elif(user_option == "3"):
                 showPandL()     
        except EOFError:
                continue    
        
"""
Selection of Trade will trigger this method.
Based on User Selection, Buy or Sell is triggered.
"""

def doTrade():
    print("\n[1] Buy")
    print("[2] Sell")
    option = input("Buy or Sell? --> ")
    if(option == "1"):
        performBuy()
    else:
        performSell()
        
"""
This method triggers methods for Buying Various Stocks.
"""        
def performBuy():
    selectstock()
    symbol = input("Enter the Stock Symbol -->")
    stockvalue = input("Enter the Stock Value -->")
    #price = input("Enter the Stock Price -->")
    if(symbol=="1"):
        price = get_quote("AAPL")
        #price = input("Enter the Stock Price -->")
        appletransaction(price, stockvalue, symbol)
    elif(symbol== "2"):
        price = get_quote("AMZN")
        amazontransaction(price, stockvalue, symbol)
    elif(symbol == "3"):
        price = get_quote("MSFT")
        microsofttransaction(price, stockvalue, symbol)
    elif(symbol == "4"):
        price = get_quote("INTC")
        intctransaction(price, stockvalue, symbol)
    else:
        price = get_quote("SNAP")
        snaptransaction(price, stockvalue, symbol)
    #showPandL()
    
def performSell():
    print("Sell")
    selectstock()
    symbol = input("Enter the Stock Symbol -->")
    stockvalue = input("Enter the Stock Value -->")
    #price = input("Enter the Stock Price -->")
    #price = get_quote(symbol)
    #price = float(price)
    if(symbol=="1"):
        price = get_quote("AAPL")
        price = input("Enter the Stock Price -->")
        appleSelltransaction(price, stockvalue, symbol)
    elif(symbol=="2"):
        price = get_quote("AMZN")
        amazonselltransaction(price, stockvalue, symbol)   
    elif(symbol == "3"):
        price = get_quote("MSFT")
        microsoftselltransaction(price, stockvalue, symbol)
    elif(symbol == "4"):
        price = get_quote("INTC")
        intcselltransaction(price, stockvalue, symbol)
    elif(symbol == "5"):
        price = get_quote("SNAP")
        snapselltransaction(price, stockvalue, symbol)
    else:
        print("\t***  Enter Stock Option 1- 5 !  ***")
                
    #showPandL()


"""
Util Functions used for various operations.
"""   
def selectstock():
    print("\n[1] Apple Inc")
    print("[2] Amazon Inc")
    print("[3] Microsoft Inc")
    print("[4] Intel Corporation")  
    print("[5] SNAP Inc")

# Default utils function to get the rates.
def getDefaultMarketValue():
    marketlist = [get_quote("AAPL"), get_quote("AMZN"), 
                  get_quote("MSFT"),get_quote("INTC"),
                  get_quote("SNAP")]
    return marketlist

# This Util is used to scrap stock price from web.
def get_quote(symbol):
    url2 = "https://finance.yahoo.com/quote/" + symbol +"?p=" +symbol
    req = urllib.request
    page = req.urlopen(url2)
    soup = BeautifulSoup(page, 'html.parser')
    price_box = soup.find('span', attrs={'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})
    price = price_box.text
    return float(price)

# This Util function is to get the previous transaction price.
def get_prev_record_inlist(processlist):
    array = processlist[len(processlist)-2]
    return array[3]

### End of Util Functions.
    
"""
This is the function for display Blotter.
"""
def showBlotter():
    print("Blotter Method")
    global df3
    
    if(len(df2)==0):
        print("\t**********************************************")
        print("\t***  Blotter Empty ! Do some Transactions  ***")
        print("\t**********************************************")
    else:
        df3 = df2.append(dfama).append(dfmicro).append(dfintel).append(dfsnap)
        df3.columns = ["Side","Ticker","Volume","Price","Cost", "Time","Order"]
        df3.nlargest(50,"Order") # For now set to top 50 trasnsactions
        print(df3)
    get_user_input()
    
"""
Main Calculation methods starts. 
Apple Calculation for Sell and Buy
"""    

def appletransaction(price, stockvalue, symbol):
    global portfolioWorth 
    global applelist
    global df2
    global applewap
    global appleupl
    global appleposition
    global buyercounter
    global buyerpricecounter
    global ordercounter
    stockvalue = int(stockvalue)
    price = float(price)
    transaction = price * stockvalue
    transaction = int(transaction)
    transactionValidation(transaction)
    portfolioWorth = portfolioWorth - transaction
    #upl=transaction - (int(stockvalue)*int(get_quote(symbol)))
    ordercounter = ordercounter + 1
    applelist.append(["Buy","Apple",stockvalue,price,int(transaction),
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ordercounter])
    df2=pd.DataFrame(applelist)
    buyercounter = buyercounter + stockvalue
    buyerpricecounter = buyerpricecounter + transaction
    if(sellcounter>0):
        wapvolume = buyercounter - sellcounter
    else:
        wapvolume = buyercounter
    appleposition = wapvolume
    if(applewap==0):
        applewap=price
    else:
        numerator = appleposition * applewap
        denominator = appleposition + stockvalue
        applewap=((numerator) + transaction)/(denominator)
    # For UPL calculation checking if the price has changed from previous price    
    if(len(applelist)>0):
        previousprice = get_prev_record_inlist(applelist)
        if(previousprice != price):
            appleupl=appleposition * (price - applewap)
    #print(df2)
    get_user_input()

def appleSelltransaction(price, stockvalue, symbol):
    global portfolioWorth 
    global applelist
    global df2
    global applewap
    global appleupl
    global appleposition
    global applerpl
    global sellcounter
    global sellpricecounter
    global ordercounter
    if(appleposition==0):
        print("Please Buy Apple Stocks before Selling")
        get_user_input()
    stockvalue = int(stockvalue)
    price = float(price)
    transaction = price * stockvalue
    transaction = int(transaction)
    portfolioWorth = portfolioWorth + transaction
    sellcounter = sellcounter + stockvalue
    sellpricecounter = sellpricecounter + transaction
    ordercounter = ordercounter + 1
    applelist.append(["Sell","Apple",stockvalue ,price,transaction ,
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ordercounter])
    df2=pd.DataFrame(applelist)
    appleposition=buyercounter - sellcounter
    #print("The apple position in sell" + appleposition)
    applerpl = applerpl + (stockvalue * (price - applewap))
    # For UPL calculation checking if the price has changed from previous price
    if(len(applelist)>0):
        previousprice = get_prev_record_inlist(applelist)
        if(previousprice != price):
            appleupl=appleposition * (price - applewap)
    #print(df2)
    get_user_input()


"""
Amazon Calculation for Sell and Buy
"""    
def amazontransaction(price, stockvalue, symbol):
    global portfolioWorth 
    global amazonlist
    global dfama
    global amazonwap
    global amazonupl
    global amazonposition
    global amazonbuyer
    global amazonbuyprice
    global ordercounter
    stockvalue = int(stockvalue)
    price = float(price)
    transaction = price * stockvalue
    transaction = int(transaction)
    transactionValidation(transaction)
    portfolioWorth = portfolioWorth - transaction
    #print("transaction-->"+str(transaction))
    ordercounter = ordercounter + 1
    amazonlist.append(["Buy","Amazon",stockvalue,price,transaction,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ordercounter])
    dfama = pd.DataFrame(amazonlist)
    amazonbuyer = amazonbuyer + stockvalue
    amazonbuyprice = amazonbuyprice + transaction
    if(amazonsellcounter>0):
        wapvolume = amazonbuyer - amazonsellcounter
    else:
        wapvolume = amazonbuyer
    amazonposition=wapvolume
    if(amazonwap==0):
        amazonwap=price
    else:
        numerator = amazonposition * amazonwap
        denominator = amazonposition + stockvalue
        amazonwap=((numerator) + transaction)/(denominator)
    # For UPL calculation checking if the price has changed from previous price
    if(len(amazonlist)>0):
        previousprice = get_prev_record_inlist(amazonlist)
        if(previousprice != price):
            amazonupl=amazonposition * (price - amazonwap)
    #print(df2)
    get_user_input()
    
def amazonselltransaction(price, stockvalue, symbol):
    global portfolioWorth 
    global amazonlist
    global dfama
    global amazonwap
    global amazonupl
    global amazonrpl
    global amazonposition
    global amazonsellcounter
    global amazonsellpricecounter
    global ordercounter
    if(amazonposition==0):
        print("Please Buy Amazon Stocks before Selling")
        get_user_input()
    stockvalue = int(stockvalue)
    price = float(price)
    transaction = price * stockvalue
    transaction = int(transaction)
    portfolioWorth = portfolioWorth + transaction
    amazonsellcounter = amazonsellcounter + stockvalue
    amazonsellpricecounter = amazonsellpricecounter + transaction
    ordercounter = ordercounter + 1
    amazonlist.append(["Sell","Amazon",stockvalue,price,transaction,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                       ,ordercounter])
    dfama = pd.DataFrame(amazonlist)
    amazonposition=amazonbuyer - amazonsellcounter
    amazonrpl = amazonrpl + (stockvalue*(price-amazonwap))
    if(len(amazonlist)>0):
        previousprice = get_prev_record_inlist(amazonlist)
        if(previousprice != price):
            amazonupl=amazonposition * (price - amazonwap)
    #print(df2)
    get_user_input()


"""
Microsoft Calculation for Sell and Buy
""" 
def microsofttransaction(price, stockvalue, symbol):
    global portfolioWorth 
    global microlist
    global dfmicro
    global microwap
    global microupl
    global microposition
    global microbuyer
    global microbuyprice
    global ordercounter
    stockvalue = int(stockvalue)
    price = float(price)
    transaction = price * stockvalue
    transaction = int(transaction)
    transactionValidation(transaction)
    portfolioWorth = portfolioWorth - transaction
    #print("transaction-->"+str(transaction))
    ordercounter = ordercounter + 1
    microlist.append(["Buy","Microsoft",stockvalue,price,transaction,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ordercounter])
    dfmicro = pd.DataFrame(microlist)
    microbuyer = microbuyer + stockvalue
    microbuyprice = microbuyprice + transaction
    if(microsellcounter>0):
        wapvolume = microbuyer - microsellcounter
    else:
        wapvolume = microbuyer
    microposition=wapvolume
    if(microwap==0):
        microwap=price
    else:
        numerator = microposition * microwap
        denominator = microposition + stockvalue
        microwap=((numerator) + transaction)/(denominator)
    if(len(microlist)>0):
        previousprice = get_prev_record_inlist(microlist)
        if(previousprice != price):
            microupl=microposition * (price - microwap)
    #print(df2)
    get_user_input()
    
def microsoftselltransaction(price, stockvalue, symbol):
    global portfolioWorth 
    global microlist
    global dfmicro
    global microwap
    global microupl
    global microrpl
    global microposition
    global microsellcounter
    global microsellpricecounter
    global ordercounter
    if(microposition==0):
        print("Please Buy Microsoft Stocks before Selling")
        get_user_input()
    stockvalue = int(stockvalue)
    price = float(price)
    transaction = price * stockvalue
    transaction = int(transaction)
    portfolioWorth = portfolioWorth + transaction
    microsellcounter = microsellcounter + stockvalue
    microsellpricecounter = microsellpricecounter + transaction
    ordercounter = ordercounter + 1
    microlist.append(["Sell","Microsoft",stockvalue,price,transaction,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                       ,ordercounter])
    dfmicro = pd.DataFrame(microlist)
    microposition=microbuyer - microsellcounter
    microrpl = microrpl + (stockvalue*(price-microwap))
    if(len(microlist)>0):
        previousprice = get_prev_record_inlist(microlist)
        if(previousprice != price):
            microupl=microposition * (price - microwap)
    #print(df2)
    get_user_input()

"""
Intel Calculation for Sell and Buy
""" 
    
def intctransaction(price, stockvalue, symbol):
    global portfolioWorth 
    global intellist
    global dfintel
    global intelwap
    global intelupl
    global intelposition
    global intelbuyer
    global intelbuyprice
    global ordercounter
    stockvalue = int(stockvalue)
    price = float(price)
    transaction = price * stockvalue
    transaction = int(transaction)
    transactionValidation(transaction)
    portfolioWorth = portfolioWorth - transaction
    #print("transaction-->"+str(transaction))
    ordercounter = ordercounter + 1
    intellist.append(["Buy","Intel",stockvalue,price,transaction,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ordercounter])
    dfintel = pd.DataFrame(intellist)
    intelbuyer = intelbuyer + stockvalue
    intelbuyprice = intelbuyprice + transaction
    if(intelsellcounter>0):
        wapvolume = intelbuyer - intelsellcounter
    else:
        wapvolume = intelbuyer
    intelposition=wapvolume
    if(intelwap==0):
        intelwap=price
    else:
        numerator = intelposition * intelwap
        denominator = intelposition + stockvalue
        intelwap=((numerator) + transaction)/(denominator)
    if(len(intellist)>0):
        previousprice = get_prev_record_inlist(intellist)
        if(previousprice != price):
            intelupl=intelposition * (price - intelwap) 
    #print(df2)
    get_user_input()
    
def intcselltransaction(price, stockvalue, symbol):
    global portfolioWorth 
    global intellist
    global dfintel
    global intelwap
    global intelupl
    global intelrpl
    global intelposition
    global intelsellcounter
    global intelsellpricecounter
    global ordercounter
    if(intelposition==0):
        print("Please Buy Intel Stocks before Selling")
        get_user_input()
    stockvalue = int(stockvalue)
    price = float(price)
    transaction = price * stockvalue
    transaction = int(transaction)
    portfolioWorth = portfolioWorth + transaction
    intelsellcounter = intelsellcounter + stockvalue
    intelsellpricecounter = intelsellpricecounter + transaction
    ordercounter = ordercounter + 1
    intellist.append(["Sell","Intel",stockvalue,price,transaction,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                       ,ordercounter])
    dfintel = pd.DataFrame(intellist)
    intelposition=intelbuyer - intelsellcounter
    intelrpl = intelrpl + (stockvalue*(price-intelwap))
    #Checking if there is a change in price.
    if(len(intellist)>0):
        previousprice = get_prev_record_inlist(intellist)
        if(previousprice != price):
            intelupl=intelposition * (price - intelwap)
    #print(df2)
    get_user_input()

"""
SNAP Calculation for Sell and Buy
""" 
    
def snaptransaction(price, stockvalue, symbol):
    global portfolioWorth 
    global snaplist
    global dfsnap
    global snapwap
    global snapupl
    global snapposition
    global snapbuyer
    global snapbuyprice
    global ordercounter
    stockvalue = int(stockvalue)
    price = float(price)
    transaction = price * stockvalue
    transaction = int(transaction)
    transactionValidation(transaction)
    portfolioWorth = portfolioWorth - transaction
    #print("transaction-->"+str(transaction))
    ordercounter = ordercounter + 1
    snaplist.append(["Buy","SNAP",stockvalue,price,transaction,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ordercounter])
    dfsnap = pd.DataFrame(snaplist)
    snapbuyer = snapbuyer + stockvalue
    snapbuyprice = snapbuyprice + transaction
    if(snapsellcounter>0):
        wapvolume = snapbuyer - snapsellcounter
    else:
        wapvolume = snapbuyer
    snapposition=wapvolume
    if(snapwap==0):
        snapwap=price
    else:
        numerator = snapposition * snapwap
        denominator = snapposition + stockvalue
        snapwap=((numerator) + transaction)/(denominator)
    if(len(snaplist)>0):
        previousprice = get_prev_record_inlist(snaplist)
        if(previousprice != price):
            snapupl=snapposition * (price - snapwap)
    #print(df2)
    get_user_input()
    
def snapselltransaction(price, stockvalue, symbol):
    global portfolioWorth 
    global snaplist
    global dfsnap
    global snapwap
    global snapupl
    global snaprpl
    global snapposition
    global snapsellcounter
    global snapsellpricecounter
    global ordercounter
    if(snapposition==0):
        print("Please Buy SNAP Stocks before Selling")
        get_user_input()
    stockvalue = int(stockvalue)
    price = float(price)
    transaction = price * stockvalue
    transaction = int(transaction)
    portfolioWorth = portfolioWorth + transaction
    snapsellcounter = snapsellcounter + stockvalue
    snapsellpricecounter = snapsellpricecounter + transaction
    ordercounter = ordercounter + 1
    snaplist.append(["Sell","SNAP",stockvalue,price,transaction,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                       ,ordercounter])
    dfsnap = pd.DataFrame(snaplist)
    snapposition=snapbuyer - snapsellcounter
    snaprpl = snaprpl + (stockvalue*(price-snapwap))
    if(len(snaplist)>0):
        previousprice = get_prev_record_inlist(snaplist)
        if(previousprice != price):
            snapupl=snapposition * (price - snapwap)
    #print(df2)
    get_user_input()  
    
    
"""
This is the function for Display P/L
"""    
def showPandL():
    print("P and L Method")
    #global df2
    global applewap
    global amazonwap
    global microwap
    global intelwap
    global snapwap
    global applerpl
    global amazonrpl
    global microrpl
    global intelrpl
    global snaprpl
    global appleupl
    global amazonupl
    global microupl
    global intelupl
    global snapupl
    
    appleprice = 0.00
    amazonprice = 0.00
    microprice = 0.00
    intelprice = 0.00
    snapprice = 0.00
    
    defaultmarketvalue = getDefaultMarketValue()
    #print("defaultmarketvalue - >" +str(float(defaultmarketvalue[0])))
    
    appleprice = float(defaultmarketvalue[0])
    amazonprice = float(defaultmarketvalue[1])
    microprice = float(defaultmarketvalue[2])
    intelprice = float(defaultmarketvalue[3])
    snapprice = float(defaultmarketvalue[4])
    
    # If there is a market fluctution and based on current price upl will change
    if(appleposition > 0 and applewap > 0):
        appleupl= appleposition * (appleprice - applewap)
    if(amazonposition > 0 and amazonwap > 0):
        amazonupl=amazonposition * (amazonprice - amazonwap)
    if(microposition > 0 and microwap > 0):
        microupl=microposition * (microprice - microwap)
    if(intelposition > 0 and intelwap > 0):
        intelupl=intelposition * (intelprice - intelwap) 
    if(snapposition > 0 and snapwap > 0):
        snapupl=snapposition * (snapprice - snapwap)
        
    # Resetting all the values,when all the shares bought are sold.Full cycle
    if(appleposition==0):
        applewap=0
        applerpl=0
    elif(amazonposition == 0):
        amazonwap=0
        amazonrpl=0
    elif(microposition == 0):
        microwap=0
        microrpl=0
    elif(intelposition == 0):
        intelwap=0
        intelrpl=0
    elif(snapposition == 0):
        snapwap=0
        snaprpl=0
    #else:
     #   appleupl = appleposition*(int(defaultmarketvalue[0])-applewap)
    pandl = OrderedDict([ ('Ticker', ['AAPL', 'AMZN', 'MSFT','INTC','SNAP', "Cash"]),
          ('Position', [appleposition, amazonposition, microposition, 
                        intelposition ,snapposition, portfolioWorth ]),
          ('Market',   [appleprice,amazonprice,
                       microprice,intelprice,snapprice, 
                       ""]),
          ('WAP', [applewap, amazonwap, microwap, intelwap, snapwap, ""]),
          ('UPL', [appleupl, amazonupl, microupl, intelupl, snapupl,""]),
          ('RPL', [applerpl, amazonrpl, microrpl, intelrpl, snaprpl,""])] )
    df4 = pd.DataFrame.from_dict(pandl)
    print(df4)
    get_user_input()

# This method is used to make sure the amount used for trading
# does not exceed the portfolio amount.    
def transactionValidation(transaction):
    if(transaction > portfolioWorth):
        print("\t**********************************************")
        print("\t* Not Enough Funds In Portofolio ! Try Again *")
        print("\t**********************************************")
        get_user_input()
    
# This is the first method,that will get called.
get_title_app()   






 

    


 
    


        

    
    

