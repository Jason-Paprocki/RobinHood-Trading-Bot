#defines the trading week to start on monday
#tracks the amount of day trades per week
#only 3 day trades are allowed per 5 days
#if trades reaches that limit trades will no longer be allowed
# this is for accs with under $25,000 in the account value
def dayTrading(json, timeNow):

    #opens the json file with the logs
    with open('dayTradeSellLogs.json') as json_file:
       logsDictionary = json.load(json_file)

    if (len(logsDictionary) == 0):
