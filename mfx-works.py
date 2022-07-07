import mfx
import multiprocessing as mp
pool = mp.Pool(mp.cpu_count())

def bot1():
    bot1usdmeth = mfx.Bot('bot1', 'USDMETH')
    bot1usdmeth.main()

def bot2():
    bot2usdmeth = mfx.Bot('bot2', 'USDMETH')
    bot2usdmeth.main()

pool.apply_async(bot1())
pool.apply_async(bot2())
pool.close()
pool.join()