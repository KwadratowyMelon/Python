from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import argparse

parser = argparse.ArgumentParser(description="scraping ceny bitcoina")
parser.add_argument('-file', '--one', help = 'json file', default = 'cnn_terms_of_use.json')
args = parser.parse_args()

options = Options()
options.add_argument('--disable-notifications')

service = Service('lab4\chromedriver.exe')
driver = webdriver.Chrome(service = service, options=options)

driver.get('https://edition.cnn.com/')

driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(1)


button1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
button1.click()

button2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="footer-nav-container"]/div[5]/div/div[2]/nav/ul/li[1]/a')))
button2.click()
time.sleep(2)

elements = driver.find_elements(By.CSS_SELECTOR, 'div')

x = []
for element in elements:
    x.append(element.text)

with open(args.one, 'r+') as f:
    json.dump(x, f)

time.sleep(100)
driver.close()