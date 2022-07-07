import datetime
import math
import random
import sys
import time
import requests
import json
import numpy as np
import ttm
import time


def path():
    import os
    config_path = os.path.abspath(os.getcwd())
    bal_path = config_path + '/bal.config'
    config_path = config_path + '/status.config'
    # url='https://api.moneta-fx.com/main/user/login'
    return config_path,bal_path

def login(email, password, ip):
    url = 'https://api.moneta-fx.com/main/user/login?user={}&password={}&ip={}'.format(email, password, ip)
    header = {'Origin': 'https://moneta-fx.com'}

    while True:
        try:
            response = requests.post(url, headers=header)
            #print(response)
        except Exception as e:
            print(e)
            continue
        else:
            break
    # print("Status Code Login", response.status_code)
    # print("JSON Response Login", response.json())
    x = response.json()
    #print(x['result']['token']['access_token'])
    auth_token = x['result']['token']['access_token']
    # user_id=x['result']['token']['userId']
    user_id = x['result']['user']['id']
    #print(user_id)
    return auth_token, user_id


def order(type, auth_token, id, volume, price, pair):
    url = 'https://api.moneta-fx.com/order/place'
    header = {'access-token': auth_token, 'Content-Type': 'application/json', 'Origin': 'https://moneta-fx.com'}
    data = {'volume': volume, 'price': price, 'market': pair, 'max': True, 'userId': id, 'orderType': type}
    data = json.dumps(data)
    # print(data)
    response = requests.post(url, headers=header, data=data)

    #print("Status Code", response.status_code)
    #print("JSON Response ", response.json())
    result=0
    if response.status_code==400:
        print("Markets Blocked BY Moneta. 1 min Delay.")
        time.sleep(60)
        result=1

    return result


def cancel_order(auth_token, order_id):
    url = 'https://api.moneta-fx.com/order/cancel?orderId={}'.format(order_id)
    header = {'access-token': auth_token, 'Content-Type': 'application/json', 'Origin': 'https://moneta-fx.com'}
    # data={'volume':volume,'price':price,'market':pair,'max':True,'userId':id,'orderType':type}
    # data=json.dumps(data)
    # print(data)
    response = requests.post(url, headers=header)  # , data=data)

    print("Status Code", response.status_code)
    print("JSON Response ", response.json())
    res = response.json()
    if res['statusCode'] == 5001:
        print(res)
        sys.exit('Balance Error')
    if response.status_code == 400:
        time.sleep(60)




def get_orders(auth_token, id, page, market):
    url = 'https://api.moneta-fx.com/order/pendingOrdersByUser/{}?size=200&page={}&market={}'.format(id, page, market)
    header = {'access-token': auth_token, 'Content-Type': 'application/json', 'Origin': 'https://moneta-fx.com'}
    # data={'volume':volume,'price':price,'market':pair,'max':True,'userId':id,'orderType':type}
    # data=json.dumps(data)
    # print(data)
    response = requests.get(url, headers=header)  # , data=data)

    #print("Status Code", response.status_code)
    #print("JSON Response ", response.json())
    x = response.json()
    res = x['result']
    #print(res)
    orders_default = res['results']
    #print("Orders default:", orders_default)
    orders = []
    for order in orders_default:
        # print(order)
        # print(order['market']['market'])
        if order['market']['market'] == market:
            orders.append(order)

    # print(orders)
    return orders


def get_balance(user_id, auth_token, currency):
    url = 'https://api.moneta-fx.com/wallet/balance/user/{}'.format(user_id)
    header = {'access-token': auth_token, 'Content-Type': 'application/json', 'Origin': 'https://moneta-fx.com'}
    response = requests.get(url, headers=header)

    #print("Status Code Balance", response.status_code)
    #print("JSON Response Balance", response.json())
    x = response.json()
    #print(x['result'])
    for res in x['result']:
        #print(res['currency']['currency'],res['available'])
        if res['currency']['currency'] == currency:
            balance = res['available']
            total_balance = res['available']+res['freeze']
    return balance,total_balance


def get_price(currency, money):
    url = 'https://api.moneta-fx.com/wallet/price/today/growth'
    # header = {'access-token': auth_token, 'Content-Type': 'application/json', 'Origin': 'https://moneta-fx.com'}
    response = requests.get(url)

    # print("Status Code Balance", response.status_code)
    # print("JSON Response Balance", response.json())
    x = response.json()
    # print(x['result'])
    for res in x['result']:
        # print(res['money'], res['price'])
        if res['stock'] == currency and res['money'] == money: price = res['price']

    return price


def oracle(currency):
    if "BTC" in currency or "ETH" in currency:
        if currency=="BTCS":currency_q="BTC"
        if currency=="BTC":currency_q="BTC"
        if currency == "ETHS": currency_q = "ETH"
        if currency == "ETH": currency_q = "ETH"

        prices = json.load(open('C:/Users\DAN\PycharmProjects\moneta-fx\PRICES\prices.config', 'r'))
        price=prices[currency_q]
        print("1 {} :$ {}".format(currency, price))

    else:
        if "STB" in currency:
            prices = json.load(open('C:/Users\DAN\PycharmProjects\moneta-fx\PRICES\prices.config', 'r'))
            STB_corr = prices['STB_corr']
            price = get_price('STB', 'USDM')
        else:
            STB_corr=0
            x = requests.get('https://apilist.stabilascan.org/api/oracle/SaGDHnTDUaH9CmTE4aETwmdQNP1xGpSoVQ/rates')
            res = x.json()
            price = res['data'][currency]

        price = round(float(price)+float(price)*STB_corr,2)
        print("1 {} :$ {}".format(currency,price))


    return price

def main(email, password, ip,config_path, bot_id, auth_token, ticker, money, market, bot_id_pair, id,bal_path):
    while True:
        try:
            bot(config_path, bot_id, auth_token, ticker, money, market, bot_id_pair, id,bal_path)
        except Exception as e:
            print(e)
            time.sleep(30)
            continue

        try:
            auth_token, id = login(email, password, ip)
        except:
            time.sleep(30)
            continue

        time.sleep(30)


def market_order(ticker_money_price, order_type, auth_token, margin_bottom, margin_top, step, id,
                 min_qty_ticker, market, max_qty_ticker, bot_status,digits,qty_digits):

    margin_top=round(random.uniform(margin_top,(margin_top+0.02)),2)
    orders = get_orders(auth_token, id, 0, market)
    #print(orders)
    print(len(orders))
    if len(orders)==0:
        margin_bottom=round(random.uniform(margin_bottom,0),3)
        margin_top=round(random.uniform(0.02,margin_top),3)
        step=step
    if len(orders) > 6 and len(orders)<12:
        margin_bottom = round(random.uniform(margin_bottom,0),3)
        margin_top = round(random.uniform(0,margin_top/2),3)
        step = step
    if len(orders) > 16 and len(orders) < 24:
        margin_bottom = round(random.uniform(margin_bottom,0),3)
        margin_top = 0.00 #round(random.uniform(0,margin_bottom/3),3)
        step = step
    if len(orders) > 24 and len(orders) < 30:
        margin_bottom = round(margin_bottom-step, 3)
        margin_top = margin_bottom  # round(random.uniform(0,margin_bottom/3),3)
        step = step



    if len(orders) > 45:
        time.sleep(30)
        return bot_status, order_type


    for i in np.arange(margin_bottom, margin_top, step):
        #print(i)
        if order_type == 'BUY':
            price = round((ticker_money_price - ticker_money_price * i), digits)
        else:
            if order_type == 'SELL':
                price = round((ticker_money_price + ticker_money_price * i), digits)

        if round(i, 2) < -0.01: qty = round(random.uniform((max_qty_ticker/2), (max_qty_ticker)), qty_digits)
        if round(i, 2) >= -0.01 and i < 0: qty = round(random.uniform((min_qty_ticker), (max_qty_ticker/2)), qty_digits)
        if round(i, 2) >= 0 and i < 0.01: qty = round(random.uniform((min_qty_ticker), max_qty_ticker), qty_digits)
        if round(i, 2) >= 0.01 and i < 0.02: qty = round(random.uniform((max_qty_ticker), (max_qty_ticker*2)),
                                                             qty_digits)
        if round(i, 2) >= 0.02 and i < 0.03: qty = round(random.uniform((max_qty_ticker), (max_qty_ticker*4)),
                                                             qty_digits)
        if round(i, 2) >= 0.03: qty = round(random.uniform((max_qty_ticker), max_qty_ticker*8), qty_digits)

        coefm = ttm.qty_time_coef(market)
        #print("Coef Qty:", coefm)
        #print("Original Qty:", qty)
        qty=round(qty*coefm,qty_digits)
        #print("QTY * Coefm:", qty)
        print("Current price:", ticker_money_price, " Order price:", price, " QTY:", qty, " I:", round(i, 2))



        res=order(order_type, auth_token, id, qty, price, market)
        if res!=0: time.sleep(random.uniform(60))
        else: time.sleep(random.uniform(2,5))


    return bot_status, order_type


def cancel_orders(bot_status, bot_id, orders, ticker_money_price, auth_token, max_sec_hold_order):
    #time.sleep(1)

    for order in orders:

        if bot_status[bot_id] == 'SELL':
            if order['price'] < ticker_money_price:
                cancel_order(auth_token, order['orderId'])
        else:
            if bot_status[bot_id] == 'BUY':
                if order['price'] > ticker_money_price:
                    cancel_order(auth_token, order['orderId'])


        time.sleep(1)

        ts = math.trunc(time.time())
        #print(ts, order['timestamp']/1000)
        delta = ts-order['timestamp']/1000
        #print("DELTA:",delta)


        if bot_status[bot_id] == 'SELL':
            if delta > max_sec_hold_order:
                cancel_order(auth_token, order['orderId'])
        else:
            if bot_status[bot_id] == 'BUY':
                if delta > max_sec_hold_order:
                    cancel_order(auth_token, order['orderId'])
        time.sleep(0.1)


def init(bot_status, auth_token, bot_id, market, id, config_path, ticker, money, bal_path, order_type):
    if 'INIT' in bot_status[bot_id]:
        orders = get_orders(auth_token, id, 0, market)
        while len(orders) != 0:
            for order in orders:
                cancel_order(auth_token, order['orderId'])
                time.sleep(0.3)
                orders = get_orders(auth_token, id, 0, market)
            print("INIT orders:", orders)
        print("Clear")
        print(bot_status[bot_id+'_roll'])

        if 'BUY' in bot_status[bot_id] and bot_status[bot_id+'_roll']==0:
            bot_status[bot_id] = 'SELL'
            bot_status[bot_id+'_roll']=1
        if 'SELL' in bot_status[bot_id] and bot_status[bot_id+'_roll']==0:
            bot_status[bot_id] = 'BUY'
            bot_status[bot_id+'_roll'] = 1

        if bot_status['bot1_roll']==1 and bot_status['bot2_roll']==1:
            bot_status['bot1_roll'] = 0
            bot_status['bot2_roll'] = 0

        with open(config_path, 'w') as outfile:
            json.dump(bot_status, outfile)

    if 'T1' in bot_status[bot_id]:

        orders = get_orders(auth_token, id, 0, market)
        while len(orders)!=0:

            print("T1 Market:", market)
            print("T1 orders:", orders)
            for order in orders:
                cancel_order(auth_token, order['orderId'])
                time.sleep(0.01)

            orders = get_orders(auth_token, id, 0, market)
        print("T1 orders:", orders)

        balances(id, auth_token, ticker, money, bal_path, order_type)

        if 'BUY' in bot_status[bot_id]:
            bot_status[bot_id] = 'BUY'
        if 'SELL' in bot_status[bot_id]:
            bot_status[bot_id] = 'SELL'
        with open(config_path, 'w') as outfile:
            json.dump(bot_status, outfile)

        sys.exit('T1 procedure active')

def balances(id, auth_token,ticker,money,bal_path, order_type):
    ticker_balance, total_ticker_balance = get_balance(id, auth_token, ticker)
    # print('aici')

    money_balance, total_money_balance = get_balance(id, auth_token, money)
    print("Ticker {} Balance:".format(ticker), ticker_balance)
    print("Money {} Balance:".format(money), money_balance)

    balance_exp = json.load(open(bal_path, 'r'))
    if "BUY" in order_type: temp_order_type="BUY"
    if "SELL" in order_type: temp_order_type = "SELL"
    balance_exp[temp_order_type][ticker] = total_ticker_balance
    balance_exp[temp_order_type][money] = total_money_balance
    with open('bal.config', 'w') as outfile:
        json.dump(balance_exp, outfile)

    return ticker_balance, money_balance



def bot(config_path,bot_id,auth_token,ticker,money,market,bot_id_pair,id,bal_path):
    while True:
        bot_status = json.load(open(config_path, 'r'))
        order_type = bot_status[bot_id]
        #print('aici')
        prices_status=json.load(open("C:/Users\DAN\PycharmProjects\moneta-fx\PRICES\prices.config", 'r'))
        if prices_status['T1'] == 'True':
            if "T1" or "INIT" not in bot_status[bot_id_pair] and "T1" or "INIT" not in bot_status[bot_id]:
                bot_status[bot_id_pair] = bot_status[bot_id_pair]+'T1'
                bot_status[bot_id] = bot_status[bot_id]+'T1'
                with open('status.config', 'w') as outfile:
                    json.dump(bot_status, outfile)


        if "INIT" or "T1" in order_type:
            init(bot_status, auth_token, bot_id, market, id, config_path,ticker, money, bal_path, order_type)
            bot_status = json.load(open(config_path, 'r'))
            order_type = bot_status[bot_id]

        #print('aici')
        margin_bottom = bot_status[order_type]['margin_bottom']
        margin_top = bot_status[order_type]['margin_top']
        step = bot_status[order_type]['step']
        min_qty_dollar = bot_status[order_type]['min_qty_dollar']
        max_qty_dollar = bot_status[order_type]['max_qty_dollar']
        max_sec_hold_order = bot_status[order_type]['max_sec_hold_order']
        freq = bot_status[order_type]['freq']
        digits=bot_status['digits']
        qty_digits = bot_status['qty_d']
        init_trigger_buy=bot_status['BUY']['init_trigger']

        #print('aici')


        ticker_balance, total_ticker_balance = get_balance(id, auth_token, ticker)
        # print('aici')

        money_balance, total_money_balance = get_balance(id, auth_token, money)
        print("Ticker {} Balance:".format(ticker), ticker_balance)
        print("Money {} Balance:".format(money), money_balance)

        ticker_oracle_price = oracle(ticker)
        money_oracle_price = oracle(money)
        #print("{} Oracle:".format(money), money_oracle_price)
        #print("{} Oracle:".format(ticker), ticker_oracle_price)
        ticker_money_price = round((ticker_oracle_price / money_oracle_price),digits)
        print("1 {} price is {}:".format(ticker, money), ticker_money_price)
        print("Market:", market)
        print(ticker, money)
        #print('aici')
        if ticker == "STB" and money == "USDM":
            vec_tri = bot_status['BUY']['vector_trigger']
            vec_tri_sale = bot_status['SELL']['vector_trigger']
            n = 0.5



        if ticker=="STB" and money=="USDM" and bot_status['BUY']['cycle'] ==0:

            print("Up Cycle")
            print(ticker_money_price)
            print(bot_status['BUY']['vector_trigger'])

            if (order_type=="BUY" and ticker_money_price< (vec_tri_sale)):
                print(111)
                bot_status['BUY']['vector'] = 'up'
                vec_delta = vec_tri_sale-ticker_money_price
                print("Vector Delta:",vec_delta)


                if vec_delta > 2:
                    bot_status['BUY']['margin_bottom'] = -0.02
                if vec_delta >= 1.5 and vec_delta < 2:
                    bot_status['BUY']['margin_bottom'] = -0.015
                if vec_delta>=1 and vec_delta<1.5:
                    bot_status['BUY']['margin_bottom'] = -0.013


                if vec_delta<1 and vec_delta>0.9:
                    bot_status['BUY']['margin_bottom'] = -0.0120
                if vec_delta<0.9 and vec_delta>0.8:
                    bot_status['BUY']['margin_bottom'] = -0.01135
                if vec_delta<0.8 and vec_delta>0.7:
                    bot_status['BUY']['margin_bottom'] = -0.011420
                if vec_delta<0.7 and vec_delta>0.6:
                    bot_status['BUY']['margin_bottom'] = -0.0115
                if vec_delta<0.6 and vec_delta>0.5:
                    bot_status['BUY']['margin_bottom'] = -0.01130
                if vec_delta<0.5 and vec_delta>0.4:
                    bot_status['BUY']['margin_bottom'] = -0.01132
                if vec_delta<0.4 and vec_delta>0.3:
                    bot_status['BUY']['margin_bottom'] = -0.011415
                if vec_delta<0.3 and vec_delta>0.2:
                    bot_status['BUY']['margin_bottom'] = -0.011420
                if vec_delta<0.2 and vec_delta>0:
                    print(222)
                    bot_status['BUY']['vector'] = ''
                    bot_status['BUY']['margin_bottom'] = -0.005
                    bot_status['BUY']['cycle'] = 1

            bot_status['BUY']['max_sec_hold_order'] = 180
            bot_status['SELL']['max_sec_hold_order'] = 120
            with open('status.config', 'w') as outfile:
                json.dump(bot_status, outfile)


        if ticker == "STB" and money == "USDM" and bot_status['BUY']['cycle'] == 1:


            bot_status['BUY']['cycle'] = 2
            bot_status['BUY']['vector_trigger'] = round(random.uniform(19.00,19.50),2)
            bot_status['SELL']['vector_trigger'] = round(random.uniform(20.00, 21.00), 2)
            bot_status['BUY']['max_sec_hold_order'] = 180
            bot_status['SELL']['max_sec_hold_order'] = 180
            with open('status.config', 'w') as outfile:
                json.dump(bot_status, outfile)


        if ticker=="STB" and money=="USDM" and bot_status['BUY']['cycle'] == 2:
            print("Down Cycle")
            print("Ticker Price:",ticker_money_price)
            print("Trigger:",bot_status['BUY']['vector_trigger'])

            if order_type=="BUY" and ticker_money_price>vec_tri:
                print(111)
                bot_status['BUY']['vector'] = 'down'
                vec_delta = vec_tri-ticker_money_price
                print("Vector Delta:",vec_delta)


                if vec_delta < -2:
                    bot_status['BUY']['margin_bottom'] = -0.005
                if vec_delta <= -1.5 and vec_delta > -2:
                    bot_status['BUY']['margin_bottom'] = -0.0052
                if vec_delta<=-1 and vec_delta>-1.5:
                    bot_status['BUY']['margin_bottom'] = -0.006


                if vec_delta>-1 and vec_delta<-0.9:
                    bot_status['BUY']['margin_bottom'] = -0.00891
                if vec_delta>-0.9 and vec_delta<-0.8:
                    bot_status['BUY']['margin_bottom'] = -0.00670
                if vec_delta>-0.8 and vec_delta<-0.7:
                    bot_status['BUY']['margin_bottom'] = -0.00875
                if vec_delta>-0.7 and vec_delta<-0.6:
                    bot_status['BUY']['margin_bottom'] = -0.0089
                if vec_delta>-0.6 and vec_delta<-0.5:
                    bot_status['BUY']['margin_bottom'] = -0.0082
                if vec_delta>-0.5 and vec_delta<-0.4:
                    bot_status['BUY']['margin_bottom'] = -0.0080
                if vec_delta>-0.4 and vec_delta<-0.3:
                    bot_status['BUY']['margin_bottom'] = -0.0085
                if vec_delta>-0.3 and vec_delta<-0.2:
                    bot_status['BUY']['margin_bottom'] = -0.01
                if vec_delta>-0.2 and vec_delta<0:
                    bot_status['BUY']['margin_bottom'] = -0.0091
                if vec_delta > 0:
                    print(222)
                    bot_status['BUY']['vector'] = ''
                    bot_status['BUY']['margin_bottom'] = -0.02
                    bot_status['BUY']['cycle'] = 0

            if order_type == "BUY" and ticker_money_price < vec_tri:
                print(222)
                bot_status['BUY']['vector'] = ''
                bot_status['BUY']['margin_bottom'] = -0.02
                bot_status['BUY']['cycle'] = 0

            bot_status['BUY']['max_sec_hold_order'] = 180
            bot_status['SELL']['max_sec_hold_order'] = 120
            with open('status.config', 'w') as outfile:
                json.dump(bot_status, outfile)

        print("Order Type:", order_type)
        min_qty_ticker = round((1 / ticker_oracle_price * min_qty_dollar), digits)
        max_qty_ticker = round((1 / ticker_oracle_price * max_qty_dollar), digits)
        print("Min qty ticker:", min_qty_ticker)
        print("Max qty ticker:", max_qty_ticker)



        if 'BUY' in order_type and money_balance >init_trigger_buy:
            # print(market)
            orders = get_orders(auth_token, id, 0, market)
            #print("Before order status:", orders)
            #print("Orders:",len(orders))
            cancel_orders(bot_status, bot_id, orders, ticker_money_price, auth_token, max_sec_hold_order)

            bot_status, order_type = market_order(ticker_money_price, order_type, auth_token, margin_bottom,
                                                           margin_top, step, id, min_qty_ticker, market,
                                                  max_qty_ticker, bot_status, digits, qty_digits)
            #orders = get_orders(auth_token, id, 0, market)
            #print("After order status:",orders)

        if 'SELL' in order_type and ticker_balance >min_qty_ticker:
            # print(market)
            orders = get_orders(auth_token, id, 0, market)
            #print("Before order status:", orders)
            cancel_orders(bot_status, bot_id, orders, ticker_money_price, auth_token, max_sec_hold_order)

            bot_status, order_type = market_order(ticker_money_price, order_type, auth_token, margin_bottom,
                                                           margin_top, step, id, min_qty_ticker, market,
                                                  max_qty_ticker, bot_status, digits, qty_digits)
            #orders = get_orders(auth_token, id, 0, market)
            #print("After order status:",orders)



        #print(order_type)
        #print(money_balance)
        if 'BUY' in order_type:
            print(init_trigger_buy)
            print(money_balance)
        if 'BUY' in order_type and money_balance < init_trigger_buy:

            bot_status[bot_id] = bot_status[bot_id]+'INIT'
            bot_status[bot_id_pair] = bot_status[bot_id_pair] + 'INIT'
            with open(config_path, 'w') as outfile:
                json.dump(bot_status, outfile)
            init(bot_status, auth_token, bot_id, market, id, config_path, ticker, money, bal_path, order_type)

        coefm = ttm.qty_time_coef(market)
        freq=random.uniform(freq, freq+(freq/coefm))
        print("Sleep:",freq)
        print("________________________________________________________")
        time.sleep(freq)
