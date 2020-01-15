import robin_stocks as trader
import json

trader.login("jasonpaprocki@tutanota.com","68WtvjQqqEqoN7",store_session=True)
dict = trader.account.get_current_positions()

dictionary = trader.account.get_current_positions()
dictDump = {}
stock = "HEXO"

for item in dict:
    i = 1
    if( str(trader.get_name_by_url(item['instrument'])) == str(trader.get_name_by_symbol(stock[0]))):
        dictDump[str(trader.get_name_by_url(item['instrument'])).upper()] = str(i)
        i+=1

print(str(trader.get_name_by_symbol(stock)[0]))







with open('traderStocks.json', 'w') as outfile:
        json.dump(dict, outfile, indent = 4)


