#only 3 day trades are allowed per 5 days
#if trades reaches that limit trades will no longer be allowed
#this is for accs with under $25,000 in the account value
#looks at the past 5 days
#if there are 3 day trades in the last 5 days then return false
def dayTrading(json, timeNow):

   #opens the json file with the logs
   with open('.json') as json_file:
      logsDictionary = json.load(json_file)

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
      
      else:
         date5DaysAgo = dateNow + 29

   