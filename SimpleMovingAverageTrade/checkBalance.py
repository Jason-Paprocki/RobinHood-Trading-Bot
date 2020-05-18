#checks the balance by loading the account and returning the buying power

# TODO check if returns int?
def checkBalance():
    #dictionary with all the account data
    dictionary = trader.profiles.load_account_profile()
    return dictionary["buying_power"]