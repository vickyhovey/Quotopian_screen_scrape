import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
CHROME_PATH = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
CHROMEDRIVER_PATH = "C:/ProgramData/Anaconda3/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe"
chrome_options = Options()
#chrome_options = webdriver.ChromeOptions()
chrome_options.set_headless(True) #make webdriver run in backgroud without showing up
chrome_options.add_argument('--no-sandbox') 
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36')
driver = webdriver.Chrome(executable_path='C:/ProgramData/Anaconda3/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe',chrome_options=chrome_options)


from selenium.webdriver.common.keys import Keys


email=input("Input your email: ")
password=input("Input your password: ")


driver.get("https://www.quantopian.com/users/sign_in")
driver.find_element_by_id("user_email").clear()
driver.find_element_by_id("user_email").send_keys(email)
driver.find_element_by_id("user_password").clear()
driver.find_element_by_id("user_password").send_keys(password)
driver.find_element_by_id("remember-checkbox").click()
driver.find_element_by_id("login-button").click()


with open('ticker.json') as data_file:    
    ticker_raw = json.load(data_file)


tickers=ticker_raw['data']


driver.get("https://www.quantopian.com/live_algorithms/5ac3d01908ce8f66c9c91930/get_latest_charts")

time.sleep(5)
raw=driver.page_source
raw_clean=raw.split(" ")[3].split("<")[0]


with open('data.json', 'w') as f:
    json.dump(raw_clean, f)
with open('data.json') as data_file:    
    data = json.load(data_file)


orders=json.loads(data)['data']['data']


positions=[]
dates=[]
for order in orders:
    positions.append(order['p'])
    dates.append(order['d'])


positions=[x for x in positions if x!=[]]



for i in range(len(positions)):
    position=positions[i]
    date=time.ctime(dates[i]/1000.0)
    shares=[None]*len(position)
    security=[None]*len(position)
    price=[None]*len(position)
    value=[None]*len(position)
    avg=[None]*len(position)
    unrealized=[None]*len(position)
    with open("orders"+str(i)+".csv", "w",newline="") as csvfile:
        fieldnames = ['Date','Security', 'Shares', 'Price', 'Avg Cost', 'Value', 'Unrealized']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for j in range(len(position)):
            #print(tickers[str(positions[j]['s'])][0]+" "+str(positions[j]['a'])+" "+str(positions[j]['ls'])+" "+str(positions[j]['cb']))
            #writer.writerow({'Security': security[i], 'Shares': str(shares[i]), 'Price': str(price[i]), 'Avg Cost': str(avg[i]), 'Value': str(value[i]), 'Unrealized': str(unrealized[i])})
            shares[j]=position[j]['a']
            security[j]=tickers[str(position[j]['s'])][0]
            avg[j]=position[j]['cb']
            price[j]=position[j]['ls']
            value[j]=position[j]['ls']*position[j]['a']
            unrealized[j]=position[j]['ls']-position[j]['cb']
            writer.writerow({'Date': date, 'Security': str(security[j]), 'Shares': str(shares[j]), 'Price': str(price[j]), 'Avg Cost': str(avg[j]), 'Value': str(value[j]), 'Unrealized': str(unrealized[j])})


data_file.close

