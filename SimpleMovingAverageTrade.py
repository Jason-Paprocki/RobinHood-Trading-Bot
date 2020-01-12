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

def movingAverage(json, stock):
    #initialization variables
    dataPriceList = []
    SimpleMovingAverageDictionary = {}

    #the ticker symbol
    #can be day week year or 5year
    #extended or regular
    #this is all the data for a specific stock for a week
    allDataDictionary = trader.stocks.get_historicals(stock, span = "week", bounds = "regular")

    #parses to get a list with just the closing price
    for i in range(len(allDataDictionary)):
        dataPriceList.append(allDataDictionary[i]["close_price"])
    
    #moving average calculation
    for i in range(len(dataPriceList)-5):
        SMA = 0
        for t in range(i,i+5):
            SMA += float(dataPriceList[t])
        SMA = SMA / 5
        SimpleMovingAverageDictionary[allDataDictionary[i+5]["begins_at"]] = str(SMA)

    #The finished dictionary ready for json dumping
    with open('MovingAverage.json', 'w') as outfile:
        json.dump(SimpleMovingAverageDictionary, outfile, indent = 4)


def availableForTrading():
    #checks if the stock market is open by making sure it is now a blacklisted date
    todayIsBlacklisted = False
    for date in BlacklistedDates:
        if( str(timeNow[0:10]) == str(date)):
            todayIsBlacklisted = True


def logClosingPrice(stock):
    #time format 2020-01-11T20:19:00.000000+00:00
    timeNow = str(zulu.now())
    
    #opens the json file with the closing prices 
    with open('Pricesper10min.json') as json_file:
        closingPricesWeekDictionary = json.load(json_file)
        

    #opens file with the dates that the stock market is closed
    with open('BlacklistedDates.json') as json_file:
            BlacklistedDates = json.load(json_file)
    
    #the moving average is calculated every 10 minutes
    #creates the next time that the log needs to happen
    hour = int(timeNow[11:13])
    currentMinute = timeNow[14:16]
    if (str(currentMinute[1:2]) == "0"):
        logTime = currentMinute
    else:
        logTime = (int(currentMinute)+10) - int(currentMinute[1:2])

    #formats the date to allow for testing
    formatedDate = str(timeNow[0:11]) + str(hour) + ":"+ str(logTime)

    #checks if the time now is the proper logging time
    if (timeNow[0:16] == formatedDate):
        #if the date is not blacklisted
        if(not todayIsBlacklisted):
            #this will format the date to match the others and then add it to the dictionary
            dateFormated = timeNow[0:16]+":00Z"
            latestPrice = str(trader.get_latest_price(stock))
            closingPricesWeekDictionary[dateFormated] = latestPrice[2:10]
    
    #opens json file with the closing prices
    with open('Pricesper10min.json', 'w') as outfile:
        json.dump(closingPricesWeekDictionary, outfile, indent = 4)

def buy(stock):
    #opens the json file with the moving average
    with open('MovingAverage.json') as json_file:
        MovingAverageDictionary = json.load(json_file)
    
    MovingAverages = []
    lastMovingAveragePrice = 0
    #finds the last moving average price
    for key in MovingAverageDictionary:
        MovingAverages.append(MovingAverageDictionary[key])
    lastMovingAveragePrice = MovingAverages[len(MovingAverages)-1]

    #open file to gather the last few prices
    with open('Pricesper10min.json') as json_file:
        Pricesper10min = json.load(json_file)

    pricesLast10min = []
    for key in MovingAverageDictionary:
        pricesLast10min.append(Pricesper10min[key])
    
    lastPrice = pricesLast10min[len(pricesLast10min)-1]
    secondTolastPrice = pricesLast10min[len(pricesLast10min)-2]

    if (lastPrice > lastMovingAveragePrice and secondTolastPrice <  lastMovingAveragePrice):
        trader.orders.order_buy_limit(stock, 1, lastPrice, timeInForce = "gfd")
        print("Noice")

def sell(stock):
    #opens the json file with the moving average
    with open('MovingAverage.json') as json_file:
        MovingAverageDictionary = json.load(json_file)
    
    MovingAverages = []
    lastMovingAveragePrice = 0
    #finds the last moving average price
    for key in MovingAverageDictionary:
        MovingAverages.append(MovingAverageDictionary[key])
    lastMovingAveragePrice = MovingAverages[len(MovingAverages)-1]

    #open file to gather the last few prices
    with open('Pricesper10min.json') as json_file:
        Pricesper10min = json.load(json_file)

    pricesLast10min = []
    for key in MovingAverageDictionary:
        pricesLast10min.append(Pricesper10min[key])
    
    lastPrice = pricesLast10min[len(pricesLast10min)-1]
    secondTolastPrice = pricesLast10min[len(pricesLast10min)-2]

    if (lastPrice < lastMovingAveragePrice and secondTolastPrice > lastMovingAveragePrice):
        trader.orders.order_sell_limit(stock, 1, lastPrice, timeInForce = "gfd")


def main():
    #login first
    login()

    #define the stock we are going to use
    stock = "HEXO"
    
    
    while (True):
        timeNow = str(zulu.now())
        if(availableForTrading(timeNow)):
            currentStockPrice = trader.stocks.get_latest_price(stock)
            movingAverage(json, stock)
            logClosingPrice(stock)
    
    
    buy(stock)
    sell(stock)

main()
