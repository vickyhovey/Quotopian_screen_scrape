import requests
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


url="https://www.quantopian.com/live_algorithms/5ac3d01908ce8f66c9c91930/get_latest_orders?number_of_orders=100"



driver.get(url)
time.sleep(5)

raw=driver.page_source
raw_clean=raw.split(" ")[5].split(">")[1].split("<")[0]


with open('data.json', 'w') as f:
    json.dump(raw_clean, f)
with open('data.json') as data_file:    
    data = json.load(data_file)

orders=json.loads(data)['data']['orders']

print("Total number of orders: "+str(len(orders)))


positions=[]
dates=[]
for order in orders:
    positions.append(order['t'])
    dates.append(order['c'])


with open("orders_fills.csv", "w",newline="") as csvfile:
    fieldnames = ['Date', 'Security', 'Shares', 'Limit', 'Stop', 'Status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(orders)):
        position=positions[i][0]
        date=time.ctime(dates[i]/1000.0)
        order=orders[i]
        security=tickers[str(order['sid'])][0]
        if order['st']==1:
            status='Filled'
        else:
            status='Not Filled'
        shares=position['a']
        limit=order['l']
        stop=order['s']
        writer.writerow({'Date': date, 'Security': security, 'Shares': str(shares), 'Limit': str(limit), 'Stop': str(stop), 'Status': status})


data_file.close

