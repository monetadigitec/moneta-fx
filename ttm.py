from datetime import datetime
import pytz

morning = 1
afternoon = 0.8
evening = 0.6
night = 0.4
mon = 0.9
tue = 0.8
wed = 0.7
thu = 0.8
fri = 0.7
sat = 0.8
sun = 0.7


def qty_time_coef(market):




    if 'USDM' in market:
        tz_NY = pytz.timezone('America/New_York')
        datetime_NY = datetime.now(tz_NY)
        #print("NY time:", datetime_NY.strftime("%H:%M:%S"))
        # print(pytz.all_timezones)
        #now_now = datetime.now()
        now_hm = datetime_NY.strftime("%H:%M")
        now_day = datetime_NY.strftime("%A")
        #print(now_hm, now_day)
        # now = '11:01'
        coefm = ret_c(now_hm, now_day)
        return coefm

    if 'GBPM' in market:
        tz_London = pytz.timezone('Europe/London')
        datetime_London = datetime.now(tz_London)
        #print("London time:", datetime_London.strftime("%H:%M:%S"))

        now_hm = datetime_London.strftime("%H:%M")
        now_day = datetime_London.strftime("%A")
        #print(now_hm, now_day)
        # now = '11:01'
        coefm = ret_c(now_hm, now_day)
        return coefm

    if 'EURM' or 'CHFM' in market:
        tz_Berlin = pytz.timezone('Europe/Berlin')
        datetime_Berlin = datetime.now(tz_Berlin)
        #print("Berlin time:", datetime_Berlin.strftime("%H:%M:%S"))

        now_hm = datetime_Berlin.strftime("%H:%M")
        now_day = datetime_Berlin.strftime("%A")
        #print(now_hm, now_day)
        # now = '11:01'
        coefm = ret_c(now_hm, now_day)
        return coefm

    if 'JPYM' in market:
        tz_Tokyo = pytz.timezone('Asia/Tokyo')
        datetime_Tokyo = datetime.now(tz_Tokyo)
        #print("Tokyo time:", datetime_Tokyo.strftime("%H"))

        now_hm = datetime_Tokyo.strftime("%H:%M")
        now_day = datetime_Tokyo.strftime("%A")
        #print(now_hm, now_day)
        # now = '11:01'
        coefm = ret_c(now_hm, now_day)
        return coefm

    if 'CNYM' in market:
        tz_HongKong = pytz.timezone('HongKong')
        datetime_HongKong = datetime.now(tz_HongKong)
        #print("HongKong time:", datetime_HongKong.strftime("%H:%M:%S"))

        now_hm = datetime_HongKong.strftime("%H:%M")
        now_day = datetime_HongKong.strftime("%A")
        #print(now_hm, now_day)
        # now = '11:01'
        coefm = ret_c(now_hm, now_day)
        return coefm

    if 'STBETH' or 'STBBTC' or 'BTCBTC' or 'ETHETH' in market:
        tz_Berlin = pytz.timezone('Europe/Berlin')
        datetime_Berlin = datetime.now(tz_Berlin)
        #print("Berlin time:", datetime_Berlin.strftime("%H:%M:%S"))

        now_hm = datetime_Berlin.strftime("%H:%M")
        now_day = datetime_Berlin.strftime("%A")
        #print(now_hm, now_day)
        # now = '11:01'
        coefm = ret_c(now_hm, now_day)
        return coefm


def ret_c(time, day):
    if time >= '06:30' and time < '12:30': coefm = morning
    if time >= '12:30' and time < '17:00': coefm = afternoon
    if time >= '17:00' and time < '24:00': coefm = evening
    if time >= '00:00' and time < '06:30': coefm = night

    if 'Mon' in day: coefm = coefm * mon
    if 'Tue' in day: coefm = coefm * tue
    if 'Wed' in day: coefm = coefm * wed
    if 'Thu' in day: coefm = coefm * thu
    if 'Fri' in day: coefm = coefm * fri
    if 'Sat' in day: coefm = coefm * sat
    if 'Sun' in day: coefm = coefm * sun

    return coefm



