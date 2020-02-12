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