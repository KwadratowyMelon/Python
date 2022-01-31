import asyncio
import json
import time
import requests
from bs4 import BeautifulSoup

async def take_price(delay, what, name):
    await asyncio.sleep(delay)
    r = requests.get(what)
    soup =  BeautifulSoup(r.text, "html.parser")
    div = soup.find('div', class_ ='left')
    price = div.find_all('span')[1]
    x = (f"wartosc {name} o godzinie {time.strftime('%X')} to {price.text} PLN")
    print(x)  
    with open('test.json', 'w+') as f:
        json.dump(x, f)
    
    


async def main():
    while True:
        task1 = asyncio.create_task(
            take_price(15, "https://e-kursy-walut.pl/kurs-bitcoin/", "bitcoin"))

        task2 = asyncio.create_task(
            take_price(10, "https://e-kursy-walut.pl/kurs-ethereum/", "ethereum"))

        print(f"started at {time.strftime('%X')}")
        await asyncio.gather(task1,task2)
        print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
