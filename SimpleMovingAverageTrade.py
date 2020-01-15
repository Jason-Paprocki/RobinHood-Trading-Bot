import robin_stocks as trader
import json
import zulu
import time
import threading

def login():
    #login using the login
    #===============================================
    #u need the 2FA to login whenever it asks
    trader.login(

def checkBalance():
    #checks the balance by loading the account and returning the buying power
    dictionary = trader.profiles.load_account_profile()
    return dictionary["buying_power"]

#get prices for the past week
##prices are logged every 10 minutes since the market opens
##logs from 9:30am to 4:00pm 
#checks the current time
#calulates the next time it needs to log
#checks if the current time matches the next logging time
#if true then it logs
#if false then it doesn't
def logClosingPrice(json, timeNow, stock):
    #the ticker symbol
    #can be day week year or 5year
    #extended or regular
    #this is all the data for a specific stock for a week
    allDataDictionary = trader.stocks.get_historicals(stock, span = "week", bounds = "regular")

    #parses to get a list with just the closing price
    for i in range(len(allDataDictionary)):
        dataPriceList.append(allDataDictionary[i]["close_price"])


    #opens the json file with the closing prices as per 10 mins
    with open('Pricesper10min.json') as json_file:
        closingPricesWeekDictionary = json.load(json_file)

    #the moving average is calculated every 10 minutes
    #if the current minute is a ten then its time to log
    logNow = False
    currentMinute = timeNow[14:16]
    if (str(currentMinute[1:2]) == "0"):
        logNow = True

    #checks if the time now is the proper logging time
    if (logNow):
        #this will format the date to match the others and then add it to the dictionary
        dateFormated = timeNow[0:16]+":00Z"
        latestPrice = str(trader.get_latest_price(stock))
        closingPricesWeekDictionary[dateFormated] = latestPrice[2:10]
    
    #opens json file with the closing prices
    with open('Pricesper10min.json', 'w') as outfile:
        json.dump(closingPricesWeekDictionary, outfile, indent = 4)

#open the prices per 10 minutes file
#read from the file
#creates a list with all the closing prices
#calculate the moving average for the entire json file
#compile a dictionary with all the moving averages
#export all that data to the moving averages json file
def movingAverage(json):
    #opens the json file with the closing prices as per 10 mins
    with open('Pricesper10min.json') as json_file:
        closingPricesWeekDictionary = json.load(json_file)

    dataPriceList = []
    for key in closingPricesWeekDictionary:
        dataPriceList.append(closingPricesWeekDictionary[key])
    
    datePriceList = []
    for key in closingPricesWeekDictionary:
        datePriceList.append(key)

    #moving average calculation
    SimpleMovingAverageDictionary = {}
    for i in range(len(dataPriceList)-5):
        SMA = 0
        for t in range(i,i+5):
            SMA += float(dataPriceList[t])
        SMA = SMA / 5
        SimpleMovingAverageDictionary[datePriceList[i+5]] = str(SMA)

    #The finished dictionary ready for json dumping
    with open('MovingAverage.json', 'w') as outfile:
        json.dump(SimpleMovingAverageDictionary, outfile, indent = 4)
    
    json_file.close()
    outfile.close()

#checks the time 
#opens the blacklisted dates
#checks if the date is on a blaclisted date
#checks if the time is when the stock market is open
def availableForTrading(timeNow):
    #opens the json file with the blacklisted dates
    with open('BlacklistedDates.json') as json_file:
        blacklistedDatesDictionary = json.load(json_file)
    json_file.close()

    #checks if the stock market is open by making sure it is not a blacklisted date
    for date in blacklistedDatesDictionary:
        if( str(timeNow[0:10]) == str(date) ):
            return False
    
    #checks if time is between 9:30am and 4:00pm
    hourAndMinute = int(timeNow[11:13] + timeNow[14:16])
    if(hourAndMinute < 1430 or hourAndMinute > 2059):
        return False
    else:
        return True

#opens the moving average json file
#opens the latest prices json file
#checks if the last price crosses the last moving average from bottom to top
#if true then buy
def conditionToBuy(json, currentTime, stock, currentStockPrice):
    #opens the json file with the moving average
    with open('MovingAverage.json') as json_file:
        MovingAverageDictionary = json.load(json_file)
    
    #open file to gather the last few prices
    with open('Pricesper10min.json') as json_file:
        Pricesper10min = json.load(json_file)
    
    MovingAverages = []
    lastMovingAveragePrice = 0
    #finds the last moving average price
    for key in MovingAverageDictionary:
        MovingAverages.append(MovingAverageDictionary[key])
    lastMovingAveragePrice = MovingAverages[len(MovingAverages)-1]

    pricesLast10min = []
    for key in MovingAverageDictionary:
        pricesLast10min.append(Pricesper10min[key])
    lastPrice = pricesLast10min[len(pricesLast10min)-1]
    secondTolastPrice = pricesLast10min[len(pricesLast10min)-2]

    if (lastPrice > lastMovingAveragePrice and secondTolastPrice <  lastMovingAveragePrice):
        buy(json, currentTime, stock, currentStockPrice)
        return True
    else:
        return False

def buy(json, currentTime, stock, currentStockPrice):

    #executes the buy operation for the corresponding stock
    trader.orders.order_buy_limit(stock, 1, lastPrice)

    #open file to gather previous trades
    with open('buyLog.json') as json_file:
        Log = json.load(json_file)

    #adds the current time of the log and price and adds it to the list
    #time format 2020-01-11T20:19:00.000000+00:00
    logTime = currentTime[0:19] + "Z"
    Log[logTime] = str(currentStockPrice) 

    #writes to the json file
    with open('buyLog.json', 'w') as outfile:
        json.dump(Log, outfile, indent = 4)

#opens the moving average json file
#opens the latest prices json file
#checks if the last price crosses the last moving average from bottom to top
#if true then buy
def conditionToSell(json, currentTime, stock, currentStockPrice):
    #opens the json file with the moving average
    with open('MovingAverage.json') as json_file:
        MovingAverageDictionary = json.load(json_file)
    
    #open file to gather the last few prices
    with open('Pricesper10min.json') as json_file:
        Pricesper10min = json.load(json_file)
    
    MovingAverages = []
    lastMovingAveragePrice = 0
    #finds the last moving average price
    for key in MovingAverageDictionary:
        MovingAverages.append(MovingAverageDictionary[key])
    lastMovingAveragePrice = MovingAverages[len(MovingAverages)-1]

    pricesLast10min = []
    for key in MovingAverageDictionary:
        pricesLast10min.append(Pricesper10min[key])
    lastPrice = pricesLast10min[len(pricesLast10min)-1]
    secondTolastPrice = pricesLast10min[len(pricesLast10min)-2]

    if (lastPrice > lastMovingAveragePrice and secondTolastPrice <  lastMovingAveragePrice):
        buy(json, currentTime, stock, currentStockPrice)
        return True
    else:
        return False

#
def sell(json, currentTime, stock, currentStockPrice):

    #executes the buy operation for the corresponding stock
    trader.orders.order_sell_limit(stock, 1, lastPrice)

    #open file to gather previous trades
    with open('sellLog.json') as json_file:
        Log = json.load(json_file)

    #adds the current time of the log and price and adds it to the list
    #time format 2020-01-11T20:19:00.000000+00:00
    logTime = currentTime[0:19] + "Z"
    Log[logTime] = str(currentStockPrice) 

    #writes to the json file
    with open('sellLog.json', 'w') as outfile:
        json.dump(Log, outfile, indent = 4)



def main():
    #login first
    login()

    #define the stock we are going to use
    stock = "HEXO"
    timeNow = str(zulu.now())
    
    while (True):
        timeNow = str(zulu.now())

        if(availableForTrading(timeNow)):
            currentStockPrice = trader.stocks.get_latest_price(stock)
            logClosingPrice(timeNow, stock)
            movingAverage(json, stock)



main()
