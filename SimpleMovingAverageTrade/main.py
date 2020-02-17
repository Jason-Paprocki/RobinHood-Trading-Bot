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
        timeNow = str(zulu.now())

        if(availableForTrading(timeNow) and dayTrading()):
            currentStockPrice = trader.stocks.get_latest_price(stock)
            logClosingPrice(timeNow, stock)
            movingAverage(json, stock)

            if(conditionToBuy):
                buy()

main()