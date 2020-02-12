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