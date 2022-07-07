import math
import random
import sys
import requests
import json
import numpy as np
import ttm
import time
import pymongo
# import logging
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

user= "bots"
psw="bots022!"


class Market:
    def __init__(self, name):
        self.name = name

        myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
        mydb = myclient["MFX"]
        mycol = mydb["Markets"]
        myquery = {"market": name}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            obj = x
        # print("market 1")
        self.ticker = obj["ticker"]
        self.money = obj["money"]
        self.digits = obj["digits"]
        self.qty_d = obj["qty_d"]
        self.SELL = obj['SELL']
        self.BUY = obj['BUY']
        # print("market 2")


class Bot():
    API_URL = 'https://api.moneta-fx.com/api/v1'

    def __init__(self, bot_name, market):
        self.bot_id = bot_name
        self.market = Market(market)
        self.API_URL = self.API_URL

        if self.bot_id == "bot1":
            self.bot_id_pair = "bot2"
        if self.bot_id == "bot2":
            self.bot_id_pair = "bot1"

        myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
        mydb = myclient["MFX"]
        mycol = mydb["Bots"]
        myquerry = {"market": self.market.name, "name": self.bot_id}
        # print(myquery)
        mydoc = mycol.find(myquerry)
        # print(mydoc)
        for x in mydoc:
            # print(11, x)
            self.x = x

        self.roll = x["roll"]
        self.status = x["status"]
        self.api_key = x["api_key"]
        self.api_secret = x["api_secret"]
        # self.ip = x["ip"]
        # print(self.roll)
        # print(self.status)
        # print(self.email)
        # print(self.pwd)
        # print(self.ip)
        # print("bot init")
        # print(self.market.name)
        # print(self.bot_id)
        # self.logging_file = 'C:/Users/DAN/PycharmProjects/moneta-fx/logs/' + self.market.name + self.bot_id + '.log'
        # print(self.#logging_file)
        # logging.basicConfig(filename=self.#logging_file, format='%(asctime)s %(message)s', level=#logging.INFO)

    def _get_headers(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'X-MFX-APIKEY': self.api_key,
            'X-MFX-SIG': self.sig
        }

        return headers

    def _generate_signature(self, data):
        data = {"data": data}
        data["apiKey"] = self.api_key
        data = json.dumps(data, separators=(',', ':')).encode('UTF-8')

        #print("Signature:", data)
        # print(type(message))

        # message = data.encode()
        # print(message)

        pkb = bytes.fromhex(self.api_secret)
        privKeyObj = RSA.import_key(pkb)

        # Sign the message using the PKCS#1 v1.5 signature scheme (RSASP1)
        # msg = b'A message for signing'
        hash = SHA256.new(data)
        signer = PKCS115_SigScheme(privKeyObj)
        self.sig = signer.sign(hash).hex()
        # print("Signature:", self.sig)

    def cancel_order(self, order_id):
        data = {"orderId": order_id}
        data = json.dumps(data, separators=(',', ':')).encode('utf-8')
        url = self.API_URL + '/order/cancel'
        self._generate_signature(json.loads(data))
        header = self._get_headers()


        while True:
            try:
                response = requests.post(url, headers=header, data=data)  # , data=data)
                if response.status_code != 200:
                    print("Get Orders Service not available, retry in 60 sec.")
                    time.sleep(60)
                else:
                    break
            except Exception as e:
                print(e)
                time.sleep(60)
                continue
        #print("Status Code", response.status_code)
        #print("JSON Response ", response.json())
        res = response.json()
        if response.status_code !=200: sys.exit("Cancel order not available")

        if res['statusCode'] == 5001:
            #print(res)
            # logging.info(res)
            sys.exit('Balance Error')
        if response.status_code == 400:
            time.sleep(60)

    def place_order(self, qty, price):

        if self.status not in ["SELL","BUY"]: return 1
        data = {"market": self.market.name, "volume": qty, "price": price, "orderType": self.status}
        data = json.dumps(data, separators=(',', ':')).encode('utf-8')
        url = self.API_URL + '/order/place'
        self._generate_signature(json.loads(data))
        header = self._get_headers()


        while True:
            try:
                if self.status in ["SELL","BUY"]:

                    response = requests.post(url, headers=header, data=data)  # , data=data)
                    x = response.json()
                    if x['statusCode'] == 5000:
                        print(111)
                        print("JSON Response ", response.json())
                        return 1
                    if x['statusCode'] == 5001:
                        print(222)
                        print("JSON Response ", response.json())
                        return 1
                    if response.status_code != 200:
                        print("Place Orders Service not available, retry in 60 sec.")
                        print("JSON Response ", response.json())
                        time.sleep(60)

                    else:
                        break
                else:
                    return 1
            except Exception as e:
                print(e)
                time.sleep(60)
                continue
        #print(response)
        #print("Status Code", response.status_code)
        #print("JSON Response ", response.json())


        return 0


    def get_orders(self, page, size):
        data = {"orderStatus": "PLACED", "market": self.market.name, "page": page, "size": size}
        data = json.dumps(data, separators=(',', ':')).encode('utf-8')
        #("DATA:", data)
        url = self.API_URL + '/order/orders'
        self._generate_signature(json.loads(data))
        header = self._get_headers()
        #print(header)



        #print("Status Code", response.status_code)
        #print("JSON Response ", response.json())
        while True:
            try:
                response = requests.post(url, headers=header, data=data)  # , data=data)
                if response.status_code != 200:
                    print("Get Orders Service not available, retry in 60 sec.")
                    time.sleep(60)
                else:
                    break
            except Exception as e:
                print(e)
                time.sleep(60)
                continue

        x = response.json()
        res = x['result']
        # print(res)
        orders_default = res['results']
        # print("Orders default:", orders_default)
        orders = []
        for order in orders_default:
            # print(order)
            # print(order['market']['market'])
            if order['market']['market'] == self.market.name:
                orders.append(order)

        # print(orders)
        return orders

    def get_balance(self, currency):
        data = {}
        data = json.dumps(data)
        url = self.API_URL + '/wallet/balance'
        self._generate_signature(json.loads(data))
        header = self._get_headers()

        while True:
            try:
                response = requests.get(url, headers=header)
                if response.status_code != 200:
                    print("Get balance Service not available, retry in 60 sec.")
                    time.sleep(60)
                else: break
            except Exception as e:
                print(e)
                time.sleep(60)
                continue
        # print("Status Code Balance", response.status_code)
        #print("JSON Response Balance", response.json())
        x = response.json()
        if x['result'] == None: sys.exit("No results available")
        #print(x['result'])
        for res in x['result']:
            # print(res['currency']['currency'],res['available'])
            if res['currency']['currency'] == currency:
                balance_avail = res['available']
                balance_freeze = res['freeze']
                total_balance = balance_avail + balance_freeze
        return balance_avail, balance_freeze, total_balance

    def get_price(self, currency, money):
        data = {}
        data = json.dumps(data)
        url = self.API_URL + '/price/24h_growth'
        self._generate_signature(json.loads(data))
        header = self._get_headers()



        while True:
            try:
                response = requests.get(url, headers=header)
                if response.status_code != 200:
                    print("Get Price Service not available, retry in 60 sec.")
                    time.sleep(60)
                else: break
            except Exception as e:
                print(e)
                time.sleep(60)
                continue

        # print("Status Code Balance", response.status_code)
        # print("JSON Response Balance", response.json())
        x = response.json()
        # print(x['result'])
        for res in x['result']:
            # print(res['money'], res['price'])
            if res['stock'] == currency and res['money'] == money: price = res['price']

        return price

    def get_stats(self, currency, money):
        data = {}
        data = json.dumps(data)
        url = self.API_URL + '/price/24h_growth'
        self._generate_signature(json.loads(data))
        header = self._get_headers()

        while True:
            try:
                response = requests.get(url, headers=header)
                if response.status_code !=200:
                    print("Get Stats Service not available, retry in 60 sec.")
                    time.sleep(60)
                else:
                    break
            except Exception as e:
                print(e)
                time.sleep(60)
                continue
        # print("Status Code Balance", response.status_code)
        # print("JSON Response Balance", response.json())
        x = response.json()
        # print(x['result'])
        for res in x['result']:
            # print(res['money'], res['price'])
            if res['stock'] == currency and res['money'] == money:
                price = res['price']
                dayHigh = res['dayHigh']
                dayLow = res['dayLow']
                dayGrowth = res['dayGrowth']

        return price, dayHigh, dayLow, dayGrowth

    def oracle(self, currency):

        if "BTC" in currency or "ETH" in currency or "STB" in currency:

            myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
            mydb = myclient["MFX"]
            mycol = mydb["Prices"]
            myquerry = {"_id": 1}
            # print(myquery)
            mydoc = mycol.find(myquerry)
            # print(mydoc)
            for x in mydoc:
                # print(11, x)
                obj = x

        if "BTC" in currency or "ETH" in currency:
            if currency == "BTCS": currency_q = "BTC"
            if currency == "BTC": currency_q = "BTC"
            if currency == "ETHS": currency_q = "ETH"
            if currency == "ETH": currency_q = "ETH"

            price = obj[currency_q]
            print("1 {} :$ {}".format(currency, price))
            # logging.info("1 {} :$ {}".format(currency, price))

        else:
            if "STB" in currency:
                STB_corr = obj['STB_corr']
                price = self.get_price('STB', 'USDM')
            else:
                STB_corr = 0
                try:
                    x = requests.get('https://apilist.stabilascan.org/api/oracle/SaGDHnTDUaH9CmTE4aETwmdQNP1xGpSoVQ/rates')
                    res = x.json()
                    #print(x.json())
                    price = res['data'][currency]
                except Exception as e:
                    print(e)



            price = round(float(price) + float(price) * STB_corr, 2)
            print("1 {} :$ {}".format(currency, price))
            # logging.info("1 {} :$ {}".format(currency, price))

        return price

    def main(self):
        # logging.basicConfig(filename=self.#logging_file, encoding='utf-8', level=#logging.info)
        while True:
            self.bot()

            # try:
            #     self.bot()
            # except Exception as e:
            #     print(e)
            #     #logging.info(e)
            #     time.sleep(30)
            #     continue
            #
            # try:
            #     self.login()
            # except:
            #     time.sleep(30)
            #     continue
            #
            # time.sleep(30)

    def market_order(self, market_obj, ticker_money_price, min_qty_ticker, max_qty_ticker):

        margin_top = market_obj['margin_top']
        margin_bottom = market_obj['margin_bottom']
        step = market_obj['step']
        margin_top = round(random.uniform(margin_top, (margin_top + 0.02)), 2)
        orders = self.get_orders(1,200)
        # print(orders)
        print("Current orders:", len(orders))
        # logging.info("Current orders:%s", len(orders))
        if len(orders) == 0:
            margin_bottom = round(random.uniform(margin_bottom, 0), 3)
            margin_top = round(random.uniform(0.02, margin_top), 3)
            step = step
        if len(orders) > 6 and len(orders) < 12:
            margin_bottom = round(random.uniform(margin_bottom, 0), 3)
            margin_top = round(random.uniform(0, margin_top / 2), 3)
            step = step
        if len(orders) > 16 and len(orders) < 24:
            margin_bottom = round(random.uniform(margin_bottom, 0), 3)
            margin_top = 0.00  # round(random.uniform(0,margin_bottom/3),3)
            step = step
        if len(orders) > 24 and len(orders) < 30:
            margin_bottom = round(margin_bottom - step, 3)
            margin_top = margin_bottom  # round(random.uniform(0,margin_bottom/3),3)
            step = step

        if len(orders) > 45:
            time.sleep(30)

        for i in np.arange(margin_bottom, margin_top, step):
            # print(i)
            if self.status == 'BUY':
                price = round((ticker_money_price - ticker_money_price * i), self.market.digits)
            else:
                if self.status == 'SELL':
                    price = round((ticker_money_price + ticker_money_price * i), self.market.digits)

            # print(2222)

            if round(i, 2) < -0.01: qty = round(random.uniform((max_qty_ticker / 2), (max_qty_ticker)),
                                                self.market.qty_d)
            if round(i, 2) >= -0.01 and i < 0: qty = round(random.uniform((min_qty_ticker), (max_qty_ticker / 2)),
                                                           self.market.qty_d)
            if round(i, 2) >= 0 and i < 0.01: qty = round(random.uniform((min_qty_ticker), max_qty_ticker),
                                                          self.market.qty_d)
            if round(i, 2) >= 0.01 and i < 0.02: qty = round(random.uniform((max_qty_ticker), (max_qty_ticker * 2)),
                                                             self.market.qty_d)
            if round(i, 2) >= 0.02 and i < 0.03: qty = round(random.uniform((max_qty_ticker), (max_qty_ticker * 4)),
                                                             self.market.qty_d)
            if round(i, 2) >= 0.03: qty = round(random.uniform((max_qty_ticker), max_qty_ticker * 8), self.market.qty_d)

            # print(1978)
            coefm = ttm.qty_time_coef(self.market.name)
            # print("Coef Qty:", coefm)
            # print("Original Qty:", qty)
            qty = round(qty * coefm, self.market.qty_d)
            # print("QTY * Coefm:", qty)
            print("Current price:", ticker_money_price, " Order price:", price, " QTY:", qty, " I:", round(i, 2))
            # logging.info("Current price:%s , Order price:%s, QTY:%s, I:%s", ticker_money_price, price, qty, round(i, 2))

            res = self.place_order(qty, price)
            # print(5555)
            if res != 0:
                return
            else:
                time.sleep(random.uniform(2, 5))
            # print(2011)
        # print(2012)

    def cancel_orders(self, orders, ticker_money_price):
        # time.sleep(1)

        for order in orders:

            if self.status == 'SELL':
                if order['price'] < ticker_money_price:
                    self.cancel_order(order['orderId'])
            else:
                if self.status == 'BUY':
                    if order['price'] > ticker_money_price:
                        self.cancel_order(order['orderId'])

            time.sleep(0.1)

            ts = math.trunc(time.time())
            # print(ts, order['timestamp']/1000)
            delta = ts - order['timestamp'] / 1000
            # print("DELTA:",delta)

            if self.status == 'SELL':
                if delta > self.market.SELL['max_sec_hold_order']:
                    self.cancel_order(order['orderId'])
            else:
                if self.status == 'BUY':
                    if delta > self.market.BUY['max_sec_hold_order']:
                        self.cancel_order(order['orderId'])
            time.sleep(0.1)

    def init(self):
        print("INIT")
        # logging.info("INIT")
        if 'INIT' in self.status:
            # print(111)
            orders = self.get_orders(1,200)
            if len(orders)>0:
                #print(orders)
                for order in orders:
                    #print(order)
                    self.cancel_order(order['orderId'])
                    time.sleep(0.1)

            orders = self.get_orders(1,200)
            if len(orders)==0:
                print("Orders:{}".format(len(orders)))
                print("Cleared Succesfully")
            # logging.info("Clear")
            print("Roll:", self.roll)
            # logging.info("Roll:%s", self.roll)

            if self.roll == 0:
                if 'BUYINIT' in self.status:
                    self.status = 'SELL'
                    self.roll = 1

                if 'SELLINIT' in self.status:
                    self.status = 'BUY'
                    self.roll = 1

            if self.roll == 1:
                if 'BUYINIT' in self.status:
                    self.status = 'SELL'
                    self.roll = 0

                if 'SELLINIT' in self.status:
                    self.status = 'BUY'
                    self.roll = 0


            # if self.roll == 1:
            #    if 'BUYINIT' in self.status:
            #        self.status = 'SELL'
            #        self.roll = 0

            myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
            mydb = myclient["MFX"]
            mycol = mydb["Bots"]
            mycol.find_one_and_update({"name": self.bot_id, "market": self.market.name},
                                      {'$set': {"status": self.status, "roll": self.roll}})

            print("Status:", self.status)

        if 'T1' in self.status:

            orders = self.get_orders(1,200)
            while len(orders) != 0:

                print("T1 Market:", self.market.name)
                print("T1 orders:", orders)
                for order in orders:
                    self.cancel_order(order['orderId'])
                    time.sleep(0.01)

                orders = self.get_orders(1,200)
            print("T1 orders:", orders)
            # logging.info("T1 orders:%s", orders)

            self.balances()

            if 'BUY' in self.status:
                self.status = 'BUY'
            if 'SELL' in self.status:
                self.status = 'SELL'

            myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
            mydb = myclient["MFX"]
            mycol = mydb["Bots"]
            mycol.find_one_and_update({"name": self.bot_id, "market": self.market.name},
                                      {'$set': {"status": self.status}})
            # logging.info('T1 procedure active')
            sys.exit('T1 procedure active')

    def balances(self):
        ticker_balance_avail, ticker_balance_freeze, total_ticker_balance = self.get_balance(self.market.ticker)
        # print('aici')

        money_balance_avail, money_balance_freeze, total_money_balance = self.get_balance(self.market.money)
        print("Ticker {} Balance:".format(self.market.ticker), total_ticker_balance)
        # logging.info("Ticker {} Balance:".format(self.market.ticker), total_ticker_balance)
        print("Money {} Balance:".format(self.market.money), total_money_balance)
        # logging.info("Money {} Balance:".format(self.market.money), total_money_balance)

        myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
        mydb = myclient["MFX"]
        mycol = mydb["Bots"]
        mycol.find_one_and_update({"name": self.bot_id, "market": self.market.name},
                                  {'$set': {"ticker_balance_avail": ticker_balance_avail,
                                            "ticker_balance_freeze": ticker_balance_freeze,
                                            "ticker_balance_total": total_ticker_balance}})

        myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
        mydb = myclient["MFX"]
        mycol = mydb["Bots"]
        mycol.find_one_and_update({"name": self.bot_id, "market": self.market.name},
                                  {'$set': {"money_balance_avail": money_balance_avail,
                                            "money_balance_freeze": money_balance_freeze,
                                            "money_balance_total": total_money_balance}})

    def bot(self):
        while True:
            # print(self.auth_token)
            # print(self.user_id)

            # print('aici')

            myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
            mydb = myclient["MFX"]
            mycol = mydb["Prices"]
            myquerry = {"_id": 1}
            # print(myquery)
            mydoc = mycol.find(myquerry)
            # print(mydoc)
            for x in mydoc:
                # print(11, x)
                obj_prices = x

            myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
            mydb = myclient["MFX"]
            mycol = mydb["Markets"]
            myquerry = {"market": self.market.name}
            # print(myquery)
            mydoc = mycol.find(myquerry)
            # print(mydoc)
            for x in mydoc:
                # print(11, x)
                obj_market = x

            if self.status == "BUY":
                self.market.BUY = obj_market['BUY']
                market_obj = self.market.BUY
            else:
                if self.status == "SELL":
                    self.market.SELL = obj_market['SELL']
                    market_obj = self.market.SELL
            # print(market_obj)

            myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
            mydb = myclient["MFX"]
            mycol = mydb["Bots"]
            myquerry = {"market": self.market.name, "name": self.bot_id}
            # print(myquery)
            mydoc = mycol.find(myquerry)
            # print(mydoc)
            for x in mydoc:
                # print(11, x)
                obj_bot = x

            myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
            mydb = myclient["MFX"]
            mycol = mydb["Bots"]
            myquerry = {"market": self.market.name, "name": self.bot_id_pair}
            # print(myquery)
            mydoc = mycol.find(myquerry)
            # print(mydoc)
            for x in mydoc:
                # print(11, x)
                obj_botpair = x

            # print(111)

            self.status = obj_bot['status']

            # print(self.status)

            if obj_prices['T1'] == 'True':
                if "T1" or "INIT" not in obj_botpair["status"] and "T1" or "INIT" not in obj_bot["status"]:
                    mycol = mydb["Bots"]
                    self.status = self.status + 'T1'

                    mycol.find_one_and_update({'name': self.bot_id, "market": self.market.name},
                                              {'$set': {"status": self.status + 'T1'}})
                    mycol.find_one_and_update({'name': self.bot_id_pair, "market": self.market.name},
                                              {'$set': {"status": obj_botpair["status"] + 'T1'}})

            # print(222)
            # print(self.status)
            if "INIT" in self.status or "T1" in self.status:
                self.init()

            myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
            mydb = myclient["MFX"]
            mycol = mydb["Bots"]
            myquerry = {"market": self.market.name, "name": self.bot_id}
            # print(myquery)
            mydoc = mycol.find(myquerry)
            # print(mydoc)
            for x in mydoc:
                # print(11, x)
                obj_mybot = x

            self.roll = obj_mybot['roll']
            self.status = obj_mybot['status']

            myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
            mydb = myclient["MFX"]
            mycol = mydb["Bots"]
            myquerry = {"market": self.market.name, "name": self.bot_id_pair}
            # print(myquery)
            mydoc = mycol.find(myquerry)
            # print(mydoc)
            for x in mydoc:
                # print(11, x)
                obj_botpair = x

            # print(333)
            if self.roll == 1 and obj_botpair['roll'] == 0:
                self.init()

            if self.roll == 1 and obj_botpair['roll'] == 1:
                self.roll = 0

                mycol = mydb["Bots"]
                mycol.find_one_and_update({"name": self.bot_id, "market": self.market.name},
                                          {'$set': {"roll": self.roll}})

                mycol = mydb["Bots"]
                mycol.find_one_and_update({"name": self.bot_id_pair, "market": self.market.name},
                                          {'$set': {"roll": 0}})

            # print(444)
            self.market.BUY = obj_market['BUY']
            self.market.SELL = obj_market['SELL']

            if self.status == "BUY":
                    market_obj = self.market.BUY
            else:
                if self.status == "SELL":
                    market_obj = self.market.SELL

            min_qty_dollar = market_obj['min_qty_dollar']
            max_qty_dollar = market_obj['max_qty_dollar']
            freq = market_obj['freq']
            digits = self.market.digits
            init_trigger_buy = self.market.BUY['init_trigger']
            init_trigger_sell = self.market.SELL['init_trigger']

            # print('555')
            # self.login()
            ticker_balance_avail, ticker_balance_freeze, total_ticker_balance = self.get_balance(self.market.ticker)
            # print('666')

            myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
            mydb = myclient["MFX"]
            mycol = mydb["Bots"]
            mycol.find_one_and_update({"market": self.market.name, "name": self.bot_id},
                                      {'$set': {"ticker_balance_avail": ticker_balance_avail, "ticker_balance_freeze":
                                          ticker_balance_freeze, "ticker_balance_total": total_ticker_balance}})

            money_balance_avail, money_balance_freeze, total_money_balance = self.get_balance(self.market.money)

            myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
            mydb = myclient["MFX"]
            mycol = mydb["Bots"]
            mycol.find_one_and_update({"market": self.market.name, "name": self.bot_id},
                                      {'$set': {"money_balance_avail": money_balance_avail, "money_balance_freeze":
                                          money_balance_freeze, "money_balance_total": total_money_balance}})

            print("Ticker {} Balance:".format(self.market.ticker), total_ticker_balance)
            # logging.info("Ticker %s Balance:%s", self.market.ticker, total_ticker_balance)
            print("Money {} Balance:".format(self.market.money), total_money_balance)
            # logging.info("Money %s Balance:%s", self.market.money, total_money_balance)
            print("Init trigger buy {}:{}".format(self.market.money, init_trigger_buy))
            print("Init trigger sell {}:{}".format(self.market.ticker, init_trigger_sell))
            ticker_oracle_price = self.oracle(self.market.ticker)
            money_oracle_price = self.oracle(self.market.money)
            # print("{} Oracle:".format(money), money_oracle_price)
            # print("{} Oracle:".format(ticker), ticker_oracle_price)
            ticker_money_price = round((ticker_oracle_price / money_oracle_price), digits)
            print("1 {}: {} {}".format(self.market.ticker, self.market.money, ticker_money_price))
            # logging.info("1 %s price is %s:%s", self.market.ticker, self.market.money, ticker_money_price)
            print("Market:", self.market.name)
            # logging.info("Market:%s", self.market.name)
            # print(self.market.ticker, self.market.money)
            # #logging.info(self.market.ticker, self.market.money)
            # print(777)
            if self.market.ticker == "STB" and self.market.money == "USDM":
                vec_tri = self.market.BUY['vector_trigger']
                vec_tri_sale = self.market.SELL['vector_trigger']
                n = 0.5

            if self.market.ticker == "STB" and self.market.money == "USDM" and self.market.BUY['cycle'] == 0:

                print("Trend: Up Cycle")
                # logging.info("Up Cycle")
                print("Ticker Price:", ticker_money_price)
                # logging.info("Ticker Price:%s", ticker_money_price)
                print("Vector trigger:", self.market.BUY['vector_trigger'])
                # logging.info("Vector trigger:%s", self.market.BUY['vector_trigger'])

                if (self.status == "BUY" and ticker_money_price > (vec_tri_sale) and self.market.BUY['cycle'] == 0):
                    self.market.BUY['vector'] = ''
                    self.market.BUY['margin_bottom'] = -0.005
                    self.market.BUY['cycle'] = 1

                    self.market.BUY['max_sec_hold_order'] = 180
                    self.market.SELL['max_sec_hold_order'] = 120
                    print("Margin bottom:", self.market.BUY['margin_bottom'])
                    # logging.info("Margin bottom:%s", self.market.BUY['margin_bottom'])
                    myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
                    mydb = myclient["MFX"]
                    mycol = mydb["Markets"]
                    mycol.find_one_and_update({"market": self.market.name},
                                              {'$set': {"BUY": self.market.BUY, "SELL": self.market.SELL}})

                if (self.status == "BUY" and ticker_money_price < (vec_tri_sale) and self.market.BUY['cycle'] == 0):
                    # print(111)
                    # print(111)
                    self.market.BUY['vector'] = 'up'
                    vec_delta = vec_tri_sale - ticker_money_price
                    print("Vector Delta:", vec_delta)
                    # logging.info("Vector Delta:%s", vec_delta)

                    price, dayHigh, dayLow, dayGrowth = self.get_stats(self.market.ticker, self.market.money)
                    gr1 = 1
                    gr2 = 1
                    dayDelta = dayHigh - dayLow

                    if price < dayHigh and price < dayLow:
                        gr1 = 1.1
                        gr2 = 1.4
                    if price < dayHigh and price > dayLow and dayDelta < 1:
                        gr1 = 1.1
                        gr2 = 1.4
                    if price < dayHigh and price > dayLow and dayDelta > 1 and price < self.market.SELL[
                        'vector_trigger']:
                        gr1 = 1.1
                        gr2 = 1.2

                    print("GR1, GR2:", gr1, gr2)
                    # logging.info("GR1:%s, GR2:%s", gr1, gr2)

                    myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
                    mydb = myclient["MFX"]
                    mycol = mydb["Markets"]
                    myquerry = {"market": self.market.name}
                    # print(myquery)
                    mydoc = mycol.find(myquerry)
                    # print(mydoc)
                    for x in mydoc:
                        # print(11, x)
                        cor_up_obj = x['Cor_up']
                    cor_up_obj=json.loads(cor_up_obj)
                    #print(cor_up_obj['2'])


                    if vec_delta > 2:
                        self.market.BUY['margin_bottom'] = cor_up_obj['2']
                    if vec_delta >= 1.5 and vec_delta < 2:
                        self.market.BUY['margin_bottom'] = cor_up_obj['1.5']
                    if vec_delta >= 1 and vec_delta < 1.5:
                        self.market.BUY['margin_bottom'] = cor_up_obj['1'] * gr1

                    if vec_delta < 1 and vec_delta > 0.9:
                        self.market.BUY['margin_bottom'] = cor_up_obj['0.9'] * gr2
                    if vec_delta < 0.9 and vec_delta > 0.8:
                        self.market.BUY['margin_bottom'] = cor_up_obj['0.8'] * gr2
                    if vec_delta < 0.8 and vec_delta > 0.7:
                        self.market.BUY['margin_bottom'] = cor_up_obj['0.7'] * gr2
                    if vec_delta < 0.7 and vec_delta > 0.6:
                        self.market.BUY['margin_bottom'] = cor_up_obj['0.6'] * gr2
                    if vec_delta < 0.6 and vec_delta > 0.5:
                        self.market.BUY['margin_bottom'] = cor_up_obj['0.5'] * gr2
                    if vec_delta < 0.5 and vec_delta > 0.4:
                        self.market.BUY['margin_bottom'] = cor_up_obj['0.4'] * gr2
                    if vec_delta < 0.4 and vec_delta > 0.3:
                        self.market.BUY['margin_bottom'] = cor_up_obj['0.3']
                    if vec_delta < 0.3 and vec_delta > 0.2:
                        self.market.BUY['margin_bottom'] = cor_up_obj['0.2']
                    if vec_delta < 0.2 and vec_delta > 0:
                        # print(222)
                        self.market.BUY['vector'] = ''
                        self.market.BUY['margin_bottom'] = cor_up_obj['0+']
                        self.market.BUY['cycle'] = 1

                self.market.BUY['max_sec_hold_order'] = 180
                self.market.SELL['max_sec_hold_order'] = 120
                print("Margin bottom:", self.market.BUY['margin_bottom'])
                # logging.info("Margin bottom:%s", self.market.BUY['margin_bottom'])
                myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
                mydb = myclient["MFX"]
                mycol = mydb["Markets"]
                mycol.find_one_and_update({"market": self.market.name},
                                          {'$set': {"BUY": self.market.BUY, "SELL": self.market.SELL}})

            if self.market.ticker == "STB" and self.market.money == "USDM" and self.market.BUY['cycle'] == 1:
                myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user, psw), authSource="admin")
                mydb = myclient["MFX"]
                mycol = mydb["Markets"]
                myquerry = {"market": "USDMSTB"}
                # print(myquery)
                mydoc = mycol.find(myquerry)
                # print(mydoc)
                for x in mydoc:
                    # print(11, x)
                    high_val = x['high']
                    low_val = x['low']
                high_val = json.loads(high_val)
                low_val = json.loads((low_val))



                self.market.BUY['cycle'] = 2
                self.market.BUY['vector_trigger'] = round(random.uniform(low_val['l1'], low_val['l2']), 2)
                self.market.SELL['vector_trigger'] = round(random.uniform(high_val['h1'], high_val['h2']), 2)
                self.market.BUY['max_sec_hold_order'] = 180
                self.market.SELL['max_sec_hold_order'] = 180
                myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
                mydb = myclient["MFX"]
                mycol = mydb["Markets"]
                mycol.find_one_and_update({"market": self.market.name},
                                          {'$set': {"BUY": self.market.BUY, "SELL": self.market.SELL}})

            if self.market.ticker == "STB" and self.market.money == "USDM" and self.market.BUY['cycle'] == 2:
                print("Down Cycle")
                # logging.info("Down Cycle")
                print("Ticker Price:", ticker_money_price)
                # logging.info("Ticker Price:%s", ticker_money_price)
                print("Trigger:", self.market.BUY['vector_trigger'])
                # logging.info("Trigger:%s", self.market.BUY['vector_trigger'])

                if self.status == "BUY" and ticker_money_price > vec_tri and self.market.BUY['cycle'] == 2 :
                    # print(111)
                    self.market.BUY['vector'] = 'down'
                    vec_delta = vec_tri - ticker_money_price
                    print("Vector Delta:", vec_delta)
                    # logging.info("Vector Delta:%s", vec_delta)

                    myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
                    mydb = myclient["MFX"]
                    mycol = mydb["Markets"]
                    myquerry = {"market": self.market.name}
                    # print(myquery)
                    mydoc = mycol.find(myquerry)
                    # print(mydoc)
                    for x in mydoc:
                        # print(11, x)
                        cor_down_obj = x['Cor_down']
                    cor_down_obj = json.loads(cor_down_obj)

                    if vec_delta < -2:
                        self.market.BUY['margin_bottom'] = cor_down_obj['-2']
                    if vec_delta <= -1.5 and vec_delta > -2:
                        self.market.BUY['margin_bottom'] = cor_down_obj['-1.5']
                    if vec_delta <= -1 and vec_delta > -1.5:
                        self.market.BUY['margin_bottom'] = cor_down_obj['-1']

                    if vec_delta > -1 and vec_delta < -0.9:
                        self.market.BUY['margin_bottom'] = cor_down_obj['-0.9']
                    if vec_delta > -0.9 and vec_delta < -0.8:
                        self.market.BUY['margin_bottom'] = cor_down_obj['-0.8']
                    if vec_delta > -0.8 and vec_delta < -0.7:
                        self.market.BUY['margin_bottom'] = cor_down_obj['-0.7']
                    if vec_delta > -0.7 and vec_delta < -0.6:
                        self.market.BUY['margin_bottom'] = cor_down_obj['-0.6']
                    if vec_delta > -0.6 and vec_delta < -0.5:
                        self.market.BUY['margin_bottom'] = cor_down_obj['-0.5']
                    if vec_delta > -0.5 and vec_delta < -0.4:
                        self.market.BUY['margin_bottom'] = cor_down_obj['-0.4']
                    if vec_delta > -0.4 and vec_delta < -0.3:
                        self.market.BUY['margin_bottom'] = cor_down_obj['-0.3']
                    if vec_delta > -0.3 and vec_delta < -0.2:
                        self.market.BUY['margin_bottom'] = cor_down_obj['-0.2']
                    if vec_delta > -0.2 and vec_delta < 0:
                        self.market.BUY['margin_bottom'] = cor_down_obj['0-']
                    if vec_delta > 0:
                        # print(222)
                        self.market.BUY['vector'] = ''
                        self.market.BUY['margin_bottom'] = cor_down_obj['0+']
                        self.market.BUY['cycle'] = 0

                if self.status == "BUY" and ticker_money_price < vec_tri and self.market.BUY['cycle'] == 2:
                    # print(222)
                    self.market.BUY['vector'] = ''
                    self.market.BUY['margin_bottom'] = -0.02
                    self.market.BUY['cycle'] = 0

                self.market.BUY['max_sec_hold_order'] = 180
                self.market.SELL['max_sec_hold_order'] = 120
                print("Margin bottom:", self.market.BUY['margin_bottom'])
                myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
                mydb = myclient["MFX"]
                mycol = mydb["Markets"]
                mycol.find_one_and_update({"market": self.market.name},
                                          {'$set': {"BUY": self.market.BUY, "SELL": self.market.SELL}})

            print("Order Type:", self.status)
            # logging.info("Order Type:%s", self.status)
            min_qty_ticker = round((1 / ticker_oracle_price * min_qty_dollar), self.market.digits)
            max_qty_ticker = round((1 / ticker_oracle_price * max_qty_dollar), self.market.digits)
            print("Min qty ticker:", min_qty_ticker)
            # logging.info("Min qty ticker:%s", min_qty_ticker)
            print("Max qty ticker:", max_qty_ticker)
            # logging.info("Max qty ticker: %s", max_qty_ticker)

            # print(888)
            if self.status == 'BUY' and money_balance_avail > init_trigger_buy:
                # print(9999)
                # print(market)
                orders = self.get_orders(1, 200)
                # print("Before order status:", orders)
                # print("Orders:",len(orders))
                self.cancel_orders(orders, ticker_money_price)

                # print(1929)
                self.market_order(market_obj, ticker_money_price, min_qty_ticker, max_qty_ticker)
                # print(99991111)
                # orders = get_orders(auth_token, id, 0, market)
                # print("After order status:",orders)

            if self.status == 'SELL' and ticker_balance_avail > min_qty_ticker:
                # print(1111)
                orders = self.get_orders(1, 200)
                print("Before order status:", len(orders))
                self.cancel_orders(orders, ticker_money_price)

                self.market_order(market_obj, ticker_money_price, min_qty_ticker, max_qty_ticker)
                # orders = get_orders(auth_token, id, 0, market)
                # print("After order status:",orders)

            #print(999)
            # print(order_type)
            # print(money_balance)
            if self.status == 'BUY':
                print("Init trigger buy:", init_trigger_buy)
                print("Init trigger sell:", init_trigger_sell)
                # logging.info("Init trigger buy: %s", init_trigger_buy)
                print("Money balance available:", money_balance_avail)
                # logging.info("Money balance available: %s", money_balance_avail)
            if self.status == 'BUY' and money_balance_avail < init_trigger_buy:
                self.status = self.status + 'INIT'

                myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
                mydb = myclient["MFX"]
                mycol = mydb["Bots"]
                mycol.find_one_and_update({"market": self.market.name, "status": self.status},
                                          {'$set': {"status": self.status}})

                myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user,psw),authSource="admin")
                mydb = myclient["MFX"]
                mycol = mydb["Bots"]
                mycol.find_one_and_update({"market": self.market.name, "status": "SELL"},
                                          {'$set': {"status": "SELLINIT"}})

                self.init()

            if self.status == 'SELL':
                print("Init trigger buy:", init_trigger_buy)
                print("Init trigger sell:", init_trigger_sell)
                # logging.info("Init trigger buy: %s", init_trigger_buy)
                print("Ticker balance available:", ticker_balance_avail)
                # logging.info("Money balance available: %s", money_balance_avail)
            if self.status == 'SELL' and ticker_balance_avail < init_trigger_sell:
                self.status = self.status + 'INIT'

                myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user, psw), authSource="admin")
                mydb = myclient["MFX"]
                mycol = mydb["Bots"]
                mycol.find_one_and_update({"market": self.market.name, "status": self.status},
                                          {'$set': {"status": self.status}})

                myclient = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/".format(user, psw), authSource="admin")
                mydb = myclient["MFX"]
                mycol = mydb["Bots"]
                mycol.find_one_and_update({"market": self.market.name, "status": "BUY"},
                                          {'$set': {"status": "BUYINIT"}})

                self.init()


            coefm = ttm.qty_time_coef(self.market.name)
            freq = random.uniform(freq, freq + (freq / coefm))

            if 'INIT' in self.status: freq = 0

            print("Sleep:", freq)
            # logging.info("Sleep:%s", freq)
            print("________________________________________________________")
            # logging.info("________________________________________________________")
            time.sleep(freq)
