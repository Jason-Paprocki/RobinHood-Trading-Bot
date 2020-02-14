#only 3 day trades are allowed per 5 days
#if trades reaches that limit trades will no longer be allowed
#this is for accs with under $25,000 in the account value
#looks at the past 5 days
#if there are 3 day trades in the last 5 days then return false
def dayTrading(json, timeNow):

   #opens the json file with the logs
   with open('dayTradeSellLogs.json') as json_file:
      logsDictionary = json.load(json_file)

   #YYYY-MM-DD
   dateNow = timeNow[0:10]

   date5DaysAgo = timeNow[8:10]

   if (str(timeNow[5:7]) == "01" or str(timeNow[5:7]) == "03" or 
   str(timeNow[5:7]) ==  "05" or str(timeNow[5:7]) ==  "07" or 
   str(timeNow[5:7]) ==  "08" or str(timeNow[5:7]) ==  "10" or 
   str(timeNow[5:7]) == "12"):
      if(date5DaysAgo < 1):
         date5DaysAgo += 30