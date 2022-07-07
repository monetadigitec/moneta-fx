import pymongo, json

bot_status = json.load(open('status.config', 'r'))
ticker = bot_status['ticker']
money = bot_status['money']
market = money + ticker
digits=bot_status['digits']
qty_digits = bot_status['qty_d']
bot1_status = bot_status["bot1"]
bot2_status = bot_status["bot2"]
stats_buy=bot_status["BUY"]
stats_sell = bot_status["SELL"]
bot1_roll =bot_status["bot1_roll"]
bot2_roll =bot_status["bot2_roll"]

id=5
myclient = pymongo.MongoClient("mongodb://localhost:27017/")


dblist = myclient.list_database_names()
if "MFX" in dblist:
  print("The database exists.")

mydb = myclient["MFX"]
print(mydb.list_collection_names())
mycol = mydb["Markets"]
mylist = { "_id": id, "market": market, "ticker": ticker, "money": money,"digits": digits, "qty_d": qty_digits, "BUY":stats_buy,"SELL":stats_sell}
try:
  x = mycol.insert_one(mylist)
except Exception as e:
  print(e)
mycol1 = mydb["Bots"]
mybots = [
  { "_id": id*2-1,"name": "bot1", "market":market, "roll":bot1_roll, "status": bot1_status,"email": "romulus@moneta.holdings", "pwd":"romulusAlex022!","ip":"188.138.153.231","ticker_balance_avail":"","ticker_balance_freeze":"",
    "ticker_balance_total":"", "money_balance_avail":"","money_balance_freeze":"","money_balance_total":""},
  { "_id": id*2,"name": "bot2", "market":market, "roll":bot2_roll, "status": bot2_status,"email": "andyf@moneta.holdings", "pwd":"andyfAlex022!","ip":"188.138.153.231","ticker_balance_avail":"","ticker_balance_freeze":"",
    "ticker_balance_total":"", "money_balance_avail":"","money_balance_freeze":"","money_balance_total":""},
  ]
try:
  x = mycol1.insert_many(mybots)
except Exception as e:
  print(e)
