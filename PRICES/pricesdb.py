import requests
from binance.client import Client
import json
import time
import pymongo
from pymongo import ReturnDocument
user= "bots"
psw="bots022!"
api=json.load(open('api_b.config', 'r'))
api_key = api['apikey']
api_secret = api['secretkey']
client = Client(api_key, api_secret)
myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
mydb = myclient["MFX"]

while True:
    mycol = mydb["Prices"]
    myquery = {"_id": 1}
    mydoc = mycol.find(myquery)
    for x in mydoc:
        obj=x
    BTC_corr = obj['BTC_corr']
    ETH_corr = obj['ETH_corr']
    freq = obj['freq']

    btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
    eth_price = client.get_symbol_ticker(symbol="ETHUSDT")
    # print full output (dictionary)
    print("BTC:", btc_price['price'],' ',"ETH:", eth_price['price'])
    #print(BTC_corr)
    #print(ETH_corr)

    btc_new_price = round(float(btc_price['price']) + float(btc_price['price'])*BTC_corr,2)
    eth_new_price = round(float(eth_price['price']) + float(eth_price['price'])*ETH_corr,2)
    print("BTC new price:", btc_new_price, ' ', "ETH new price:", eth_new_price)

    prices_new = obj
    prices_new['BTC']=btc_new_price
    prices_new['ETH']=eth_new_price
    #quit()


    print(prices_new)
    print(mycol.find_one_and_update({'_id': 1},
                            {'$set': {"BTC": btc_new_price,"ETH": eth_new_price}},
                               return_document=ReturnDocument.AFTER))

    time.sleep(freq)