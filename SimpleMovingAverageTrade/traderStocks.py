#access the users portfolio
#pulls all the stocks currently owned by the trader
def traderStocks(json, stock):
    dictionary = trader.account.get_current_positions()
    dictDump = {}

    for item in dict:
        i = 1
        if( str(trader.get_name_by_url(item['instrument'])) == str(trader.get_name_by_symbol(stock)[0])):
            dictDump[str(trader.get_name_by_url(item['instrument'])).upper()] = str(i)
            i+=1