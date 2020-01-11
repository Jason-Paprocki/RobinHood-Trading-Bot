import robin_stocks as trader
import json
import zulu
import time
import threading

def login():
    #login using the login
    #===============================================
    #u need the 2FA to login whenever it asks
    

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

    

def getLatestPrice(stock):
    return trader.stocks.get_latest_price(stock)

def logLastClosingPrice():
    #time format 2020-01-11T20:19:00.000000+00:00
    timeNow = str(zulu.now())
    
    #opens file with the blacklisted dates
    with open('BlacklistedDates.json') as json_file:
            BlacklistedDates = json.load(json_file)
    

    allDataDictionary = trader.stocks.get_historicals("HEXO", span = "week", bounds = "regular")
    cooldict={}
    closingprice = []
    beginsat = []
    for i in range(len(allDataDictionary)):
        closingprice.append(allDataDictionary[i]["close_price"])
    for i in range(len(allDataDictionary)):
        beginsat.append(allDataDictionary[i]["begins_at"])
    for i in range(len(closingprice)):
        cooldict[beginsat[i]] = closingprice[i]
    print(cooldict)


    #opens json file with the closing prices
    with open('closingprices.json', 'w') as outfile:
        json.dump(cooldict, outfile, indent = 4)

    #checks time for 3:50pm
    while (str(timenow[11:20]) == "15:50"):
        
        #checks if the stock market is open by making sure it is now a blacklisted date
        for date in BlacklistedDates:
            if( str(timeNow[0:10]) != str(date)):
                pass


def main():
    #login first
    login()
    movingAverage(json, "HEXO")


    logLastClosingPrice()
    #loggingTheClosingPriceThread = threading.Thread(target = logLastClosingPrice)
    #loggingTheClosingPriceThread.start()
    



main()
