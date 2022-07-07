import json
import pymongo
user= "bots"
psw="bots022!"
def balance_chk(market):
    myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
    mydb = myclient["MFX"]
    mycol = mydb["Bots"]
    myquerry = {"market": market, "name": 'bot1'}
    # print(myquery)
    mydoc = mycol.find(myquerry)
    # print(mydoc)
    for x in mydoc:
        # print(11, x)
        bot1 = x
    bot1_ticker_balance_total=bot1['ticker_balance_total']
    bot1_money_balance_total = bot1['money_balance_total']

    myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
    mydb = myclient["MFX"]
    mycol = mydb["Bots"]
    myquerry = {"market": market, "name": 'bot2'}
    # print(myquery)
    mydoc = mycol.find(myquerry)
    # print(mydoc)
    for x in mydoc:
        # print(11, x)
        bot2 = x
    bot2_ticker_balance_total = bot2['ticker_balance_total']
    bot2_money_balance_total = bot2['money_balance_total']


    ticker_balance_bot=bot1_ticker_balance_total+bot2_ticker_balance_total
    money_balance_bot = bot1_money_balance_total+bot2_money_balance_total

    print("___________{}".format(market))
    print("B1&B2 [Ticker:{:15.2f}] [Money:{:15.2f}]".format(round(ticker_balance_bot,1),round(money_balance_bot,1)))

balance_chk('USDMSTB')
balance_chk('USDMBTC')
balance_chk('USDMETH')


