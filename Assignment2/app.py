# Assignment 2 template code
# Jamiel Sheikh

# Resources:
# https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972
# https://www.w3schools.com/bootstrap/default.asp
# https://www.w3schools.com/bootstrap/bootstrap_buttons.asp


from flask import Flask, render_template, request
import urllib.request as req
import pandas as pd
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime, timedelta
import plotly
from plotly.graph_objs import Scatter, Layout
import pandas_datareader.data as web
import plotly.graph_objs as go   
import numpy as np
#import os

app = Flask(__name__)

cache = False
blotterColumnNames=['Action','Cash Balance','Price','Stock Name','Time','Transaction',
                                      'Value']
pandlColumnNames = ['Symbol','Position','MarketPrice','WAP','UPL','RPL','TotalPL',
                                      'PerShareCount', 'PerDollarCount']
blotterdf = pd.DataFrame(columns=blotterColumnNames)
blotterdf = blotterdf.reindex(columns=blotterColumnNames)
pandldf =  pd.DataFrame(columns=pandlColumnNames)   
pandldf = pandldf.reindex(columns=pandlColumnNames)
ordercounter = 0
rpl = 0
upl = 0
percentageofdollar = 0
percentageofshare = 0

portfolioWorth = 10000000

# Reading from Mongo to Cache the blotter.
client = MongoClient("mongodb://dilipganesan:Appagan7883!@ds249565.mlab.com:49565/dilipganesan")
#client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
db = client['dilipganesan']
mycursor=db.blotterdf.find({},{"Action":1,"Stock Name":1,
                         "Value":1,"Price":1,"Transaction":1,"Time":1,"Cash Balance":1, "_id":0})
if(mycursor.count()>0):
    blotterdf = pd.DataFrame(list(mycursor))
    


@app.route("/")
def show_main_page():
    return render_template('main.html')

@app.route("/trade")
def show_trade_screen():
    return render_template('trade_new.html')

@app.route("/blotter")
def show_blotter():
     return render_template('sampleblotter.html', data = blotterdf.to_html(index=False))
 

@app.route("/pl")
def show_pl():
    #global pandldf
    #mycur=db.pandldf.find({},{"Symbol":1,"Position":1,
                        # "MarketPrice":1,"WAP":1,"UPL":1,"RPL":1,"TotalPL":1,"PerShareCount":1,"PerDollarCount":1, "_id":0})
    #if(mycur.count()>0):
       # pandldf = pd.DataFrame(list(mycur))
    
    return render_template('samplepl.html', data = pandldf.to_html(index=False))
    #return render_template('pl.html')

@app.route("/analytics")
def show_analytics():
    return render_template('sampleanalytics.html')

@app.route("/submitanalytics",methods=['POST'])
def execute_analytics():
    print("Inside Analytics")
    symbol = request.form['symbol']
    cacheload()
    client = MongoClient("mongodb://dilipganesan:Appagan7883!@ds249565.mlab.com:49565/dilipganesan")
    #client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
    #db = client.test
    db = client['dilipganesan']
    compdf = pd.DataFrame(list(db.companyname.find({})))
    # If we get value for Company Name good, else throw exception.
    if(compdf['Symbol'].str.contains(symbol).any()):
        print("The stock is good for trade")
    else:
        return "The Stock You are trying to Trade is not in Stock Market"
    df = web.DataReader(symbol, 'yahoo',
                    datetime.today()- timedelta(days=200),
                    datetime.today())

    # Average Calculation
    df['Average'] = df['Adj Close'].rolling(window=200, min_periods=0).mean()
    #Standard Deviation Calculation.
    df['Voltality'] = pd.Series.rolling(df['Close'], window=200,min_periods=0, center=False).std(ddof=0)
    print(df.head())
    trace_average = go.Scatter(
                x=df.index,
                y=df['Average'],
                name = "Stock Average",
                line = dict(color = '#17BECF'),
                opacity = 0.8)

    trace_sd = go.Scatter(
                x=df.index,
                y=df['Voltality'],
                name = "Stock Voltality",
                line = dict(color = '#7F7F7F'),
                opacity = 0.8)

    data = [trace_average,trace_sd]

    layout = dict(
    title = symbol+" Stock Average and Voltality",
    xaxis = dict(
        range = [datetime.today()- timedelta(days=200),datetime.today()])
    )

    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig, filename = './templates/analgraph.html',auto_open=False)
    return render_template('analoutput.html',data=df.head(n=20).to_html(index=False))


@app.route("/submitTrade",methods=['POST'])
def execute_trade():
    global portfolioWorth
    global ordercounter
    global upl
    global rpl
    global percentageofshare
    global percentageofdollar
    symbol = request.form['symbol']
    quantity = request.form['quantity']
    #price = request.form['price']
    price = get_quote(symbol)
    cacheload()
    client = MongoClient("mongodb://dilipganesan:Appagan7883!@ds249565.mlab.com:49565/dilipganesan")
    #client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
    #db = client.test
    db = client['dilipganesan']
    compdf = pd.DataFrame(list(db.companyname.find({})))
    # If we get value for Company Name good, else throw exception.
    if(compdf['Symbol'].str.contains(symbol).any()):
        print("The stock is good for trade")
    else:
        return "The Stock You are trying to Trade is not in Stock Market" 
    
    if request.form['submit'] in ('buy', 'sell'):
        #price = get_quote(symbol)
        quantity = int(quantity)
        price = float(price)
        transaction = price * quantity
        transaction = int(transaction)
    if request.form['submit']=="buy":
        print("value of buy-->")
        portfolioWorth = portfolioWorth - transaction
        ordercounter = ordercounter + 1
        buyercount = blotterdf.loc[(blotterdf['Action'] == 'buy') & 
                               (blotterdf['Stock Name'] == symbol), 'Value'].sum()
        if(np.isnan(buyercount)):
            buyercount = quantity
        else:
            buyercount = buyercount + quantity
        sellercount = blotterdf.loc[(blotterdf['Action'] == 'sell') & 
                                (blotterdf['Stock Name'] == symbol), 'Value'].sum()
        #sellercount = int(sellercount)
        #print(str(sellercount))
        if(sellercount>0):
            wapvolume = buyercount - sellercount
        else:
            wapvolume = buyercount
        position = wapvolume
        intwap = pandldf.loc[pandldf['Symbol'] == symbol, 'WAP'].tail(1)
        print(intwap)
        print(pandldf.loc[pandldf['Symbol'] == symbol, 'WAP'])
        if(intwap.any() > 0):
            numerator = (position-quantity) * pandldf.loc[pandldf['Symbol'] == symbol, 'WAP']
            print(str(numerator))
            denominator = position 
            print(str(denominator))
            wap = ((numerator) + transaction)/(denominator)
            wap = float(wap)
        else:
            wap=price
            rpl=0
        
        # For UPL calculation checking if the price has changed from previous price  
        previousprice = pandldf.loc[pandldf['Symbol'] == symbol, 'MarketPrice'].tail(1)
        #print(previousprice.to_string)
        if(previousprice.any() == True):
            #print("Inside true previous price"+str(previousprice[0]))
            #print("Inside true price"+str(price))
            if(previousprice[0] != price):
                upl=position * (price - wap)
        else:
            upl = position * (price - wap)# This means no record exist and this is new record.
        
    elif request.form['submit']=="sell":
        print("value of sell-->")
        portfolioWorth = portfolioWorth + transaction
        buyercount = blotterdf.loc[(blotterdf['Action'] == 'buy') & 
                               (blotterdf['Stock Name'] == symbol), 'Value'].sum()
        #print(str(buyercount))
        #buyercount = buyercount
        sellercount = blotterdf.loc[(blotterdf['Action'] == 'sell') & 
                                    (blotterdf['Stock Name'] == symbol), 'Value'].sum()
        if(np.isnan(sellercount)):
            sellercount = quantity
        else:
            sellercount = sellercount + quantity
        ordercounter = ordercounter + 1
        
        position = buyercount - (sellercount)
        
        intwap = pandldf.loc[pandldf['Symbol'] == symbol, 'WAP'].tail(1)
        print(intwap)
        print(pandldf.loc[pandldf['Symbol'] == symbol, 'WAP'])
        if(intwap.any() > 0):
           rpl = pandldf.loc[pandldf['Symbol'] == symbol, 'RPL'] + (quantity * (price - pandldf.loc[pandldf['Symbol'] == symbol, 'WAP'].tail(1)))
        else:
            print("Selling Before buying, not possible")
        wap=pandldf.loc[pandldf['Symbol'] == symbol, 'WAP'].tail(1)
       # if rpl.any()== True:
            #rpl=rpl[0].item()
        # For UPL calculation checking if the price has changed from previous price
        #previousprice = pandldf.loc[pandldf['Symbol'] == symbol, 'MarketPrice'].tail(1)
        #if(previousprice.any() == True):
           # if(previousprice[0] != price):
        upl=position * (price - wap)
    elif request.form['submit']=="100trades":
        firstdata=pd.DataFrame()
        lastdata=pd.DataFrame()
        fulldata = pd.DataFrame()
        print("Last 100 trades")
        url1="http://www.nasdaq.com/symbol/"+symbol+"/time-sales?pageno=1"
        page = req.urlopen(url1)
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('table', attrs={'id':'AfterHoursPagingContents_Table'})
        firstdata = parse100trades(table)
        url2="http://www.nasdaq.com/symbol/"+symbol+"/time-sales?pageno=2"
        page = req.urlopen(url2)
        soup = BeautifulSoup(page, 'html.parser')
        table2 = soup.find('table', attrs={'id':'AfterHoursPagingContents_Table'})
        lastdata = parse100trades(table2)
        fulldata = pd.concat([firstdata, lastdata]).fillna(0)
        fulldata.columns=['NLS Time','NLS Price','NLS Share Volume']
        #print(firstdata)
        #print(lastdata)
        #print(fulldata)
        return render_template('sample100trades.html', data = fulldata.to_html(index=False))
    elif request.form['submit']=="100days":
        print("Last 100 Days Trades")
        print(plotly.__version__)
        df = web.DataReader(symbol, 'yahoo',
                    datetime.today()- timedelta(days=120),
                    datetime.today())
        plotly.offline.plot({
                "data": [Scatter(x=df.index, y=df.High)],
                "layout": Layout(title=symbol+" 100 Days Plot")
                },filename='./templates/mygraph.html',auto_open=False)
        return render_template('sample100days.html')
    
    
    # Building the Blotter and P/L.
    if(pandldf['Position'].any()):
        percentageofshare=position/pandldf['Position'].sum()
        
    if(pandldf['UPL'].any()):
        percentageofdollar=upl/pandldf['UPL'].sum()
    print(rpl)
    row = [request.form['submit'],portfolioWorth,price,symbol,
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),transaction,quantity]
    row2=[symbol,position,price,wap,upl,rpl,
                      upl+rpl,percentageofshare,percentageofdollar]
    blotterdf.loc[len(blotterdf)] = row
    # Inserting Blotter to BD
    #client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],
    #27017)
    #db = client.test
    db = client['dilipganesan']
    db.blotterdf.insert_many(blotterdf.tail(1).to_dict('records'))  
    
    if(pandldf['Symbol'].str.contains(symbol).any()):
        #print("Update Already Exist")
        pandldf.loc[pandldf['Symbol'] == symbol, 1:9] = [position,price,wap,upl,rpl,upl+rpl,percentageofshare,percentageofdollar]
        
       # db.pandldf.find_one_and_update({"Symbol":symbol},{'$set':{'Position':position,'MarketPrice':price,'WAP':wap.astype(float),'UPL':upl,'RPL':rpl
                                     #  ,'TotalPL':upl+rpl,'PerShareCount':percentageofshare,'PerDollarCount':percentageofdollar}})
    else:
        #print("New Record")
        pandldf.loc[len(pandldf)] = row2
       # db.pandldf.insert_many(pandldf.tail(1).to_dict('records'))
   
    
    print(blotterdf)
    print(pandldf)

    if request.form['submit']=="buy":
        return "The Stock Of " + symbol + " Was Bought at Price->" + str(price)
    else:
        return "The Stock Of " + symbol + " Was Sold at Price->" + str(price)
# Used snippet of Bloomberg scraping as posted on Slack
def get_quote(symbol):
    url = 'https://www.bloomberg.com/quote/' + symbol + ':US'
    page = req.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    price_box = soup.find('div', attrs={'class':'price'})
    price = price_box.text
    price = price.replace(',', '')
    price = float(price)
    return price


def get_type_convert(np_type):
   convert_type = type(np.zeros(1,np_type).tolist()[0])
   return convert_type

def cacheload():
    
    global cache
    print("Cache Load Getting Called->"+str(cache))
    if cache == False:
        # load in to mongodb
        loadCSV()
        cache= True
        
def loadCSV():
    url="http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"
    c=pd.read_csv(url)   
    client = MongoClient("mongodb://dilipganesan:Appagan7883!@ds249565.mlab.com:49565/dilipganesan")
    #client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
    #db = client.test
    db = client['dilipganesan']
    db.companyname.insert_many(c.to_dict('records'))   
    
def parse100trades(table):
    row_marker = 0
    new_table = pd.DataFrame(columns=range(0,3),index=range(0,50)) # I know the size 


    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            new_table.loc[row_marker,column_marker] = column.get_text()
            column_marker += 1
            if column_marker == 3:
                row_marker += 1
        
    return new_table
    

@app.route("/main")
def show_sample():
    return render_template('sample.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True) # host='0.0.0.0' needed for docker
