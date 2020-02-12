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