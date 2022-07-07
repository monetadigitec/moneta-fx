from threading import Thread
import mfx




capturer = Thread(target=mfx.Bot('bot1', 'USDMETH').main(), daemon=True)
capturer.start()


processor = Thread(target=mfx.Bot('bot2', 'USDMETH').main(), daemon=True)
processor.start()
