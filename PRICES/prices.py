import os
from binance.client import Client
import json
import time
api=json.load(open('api_b.config', 'r'))
api_key = api['apikey']
api_secret = api['secretkey']
client = Client(api_key, api_secret)

while True:
    prices_old = json.load(open('prices.config', 'r'))
    BTC_corr = prices_old['BTC_corr']
    ETH_corr = prices_old['ETH_corr']
    freq = prices_old['freq']

    btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
    eth_price = client.get_symbol_ticker(symbol="ETHUSDT")
    # print full output (dictionary)
    print("BTC:", btc_price['price'],' ',"ETH:", eth_price['price'])
    #print(BTC_corr)
    #print(ETH_corr)

    btc_new_price = round(float(btc_price['price']) + float(btc_price['price'])*BTC_corr,2)
    eth_new_price = round(float(eth_price['price']) + float(eth_price['price'])*ETH_corr,2)
    print("BTC new price:", btc_new_price, ' ', "ETH new price:", eth_new_price)

    prices_new = prices_old
    prices_new['BTC']=btc_new_price
    prices_new['ETH']=eth_new_price
    #quit()
    print(prices_new)
    try:
        with open('prices.config', 'w') as outfile:
            json.dump(prices_new, outfile)
    except Exception as e:
        continue

    time.sleep(freq)