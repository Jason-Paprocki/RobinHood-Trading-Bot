#buy
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