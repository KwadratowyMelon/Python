from rich.console import Console 
import rich.traceback
import requests
from bs4 import BeautifulSoup
import json
import argparse
import time
import datetime

parser = argparse.ArgumentParser(description="scraping ceny bitcoina")
parser.add_argument('-file', '--one', help = 'json file', default = 'test.json')
args = parser.parse_args()

console = Console()
console.clear()
rich.traceback.install()


while True:
    r = requests.get("https://e-kursy-walut.pl/kurs-bitcoin/")
    soup =  BeautifulSoup(r.text, "html.parser")
    div = soup.find('div', class_ ='left')
    price = div.find_all('span')[1]
    x = (f"wartosc bitcoin {datetime.datetime.now()} to {price.text} PLN")
    print(x)  
    with open(args.one, 'w+') as f:
        json.dump(x, f)
    time.sleep(60)