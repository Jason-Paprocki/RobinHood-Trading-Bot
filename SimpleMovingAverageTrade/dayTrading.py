#only 3 day trades are allowed per 5 days
#if trades reaches that limit trades will no longer be allowed
#this is for accs with under $25,000 in the account value
#looks at the past 5 days
#if there are 3 day trades in the last 5 days then return false
def dayTrading(json, timeNow):

   #opens the json file with the buy logs
   with open('buyLog.json') as json_file:
      buyLogDictionary = json.load(json_file)
   #opens the json file with the sell logs
   with open('sellLog.json') as json_file:
      sellLogDictionary = json.load(json_file)

   #YYYY-MM-DD
   dateNow = timeNow[0:10]

   date5DaysAgo = timeNow[8:10] - 4
   month5DaysAgo = str(timeNow[5:7])

   if(date5DaysAgo < 1):
      month5DaysAgo -= 1

      if (month5DaysAgo == "01" or month5DaysAgo == "03" or 
      month5DaysAgo ==  "05" or month5DaysAgo ==  "07" or 
      month5DaysAgo ==  "08" or month5DaysAgo ==  "10" or 
      month5DaysAgo == "12"):
            date5DaysAgo = dateNow + 31
      
      elif (month5DaysAgo == "04" or month5DaysAgo == "06" or month5DaysAgo ==  "09" or 
      month5DaysAgo ==  "11" or month5DaysAgo ==  "10" or month5DaysAgo == "12"):
            date5DaysAgo = dateNow + 30
      
      #febuary
      else:
         date5DaysAgo = dateNow + 29

   dayTrades = 0
   for buyDate in buyLogDictionary:
      buyCompareDate = str(buyLogDictionary[buyDate])
      buyCompareDate = int(buyDate[8:10])
      if (buyCompareDate >= date5DaysAgo ):
         for sellDate in sellLogDictionary:
            sellCompareDate = str(sellLogDictionary[sellDate])
            sellCompareDate = int(sellDate[8:10])
            if(buyCompareDate == sellCompareDate):
               dayTrades +=1
      if(dayTrades == 3):
         return False
   return True
