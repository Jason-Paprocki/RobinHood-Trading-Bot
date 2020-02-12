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