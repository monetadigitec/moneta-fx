import datetime, time
import numpy as np
import requests
import json
import monetafx
import os
config_path,bal_path=monetafx.path()
email='cny@moneta.holdings'
scp='Alex022!33'
password='Alex022!'
ip='188.138.153.231'

bot_id='bot1'
bot_id_pair='bot2'


auth_token, id = monetafx.login(email, password, ip)
bot_status = json.load(open('status.config', 'r'))

ticker = bot_status['ticker']
money = bot_status['money']
market = money + ticker
roll=bot_id+'_roll'
rollover = bot_status[roll]

monetafx.main(email, password, ip,config_path, bot_id, auth_token, ticker, money, market, bot_id_pair, id, bal_path)
