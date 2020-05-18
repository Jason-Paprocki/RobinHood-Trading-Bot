#external imports
import robin_stocks as trader
import json
import zulu
import time
import threading

#internal functions
from login import *
from checkBalance import *
from traderStocks import *
from logClosingPrice import *
from movingAverage import *
from availableForTrading import *
from dayTrading import *
from conditionToBuy import *
from buy import *
from conditionToSell import *
from sell import *
from dayTrading import *

def main():
    #login first
    login()

    #define the stock we are going to use
    #ticker symbol
    stock = "HEXO"
    

    while (True):
        #gets the current time
        timeNow = str(zulu.now())

        if(availableForTrading(timeNow) and dayTrading()):
            #current stock price of the stock provided
            currentStockPrice = trader.stocks.get_latest_price(stock)

            logClosingPrice(timeNow, stock)
            movingAverage(json, stock)

            if(conditionToBuy and checkBalance > currentStockPrice):
                buy()
            
            else:
                print("cant buy")

main()