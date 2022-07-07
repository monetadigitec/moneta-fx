import requests
import asyncio

async def huinea():
    x = requests.get('https://ipapi.co/188.138.153.231/json')
    print(x)
    await asyncio.sleep(0)

async def main(tasks):

    for task in range(0,tasks):
        asyncio.create_task(huinea())



#asyncio.run(main(300))

