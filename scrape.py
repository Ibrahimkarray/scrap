from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
options = Options()

# Disabling chrome's bot mode
options.headless = True
options.add_argument('--disable-blink-features=AutomationControlled')

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(
            
            options=options
        )
xlsx_file_path = '1.xlsx'
df = pd.DataFrame()
data_frame = pd.read_excel(xlsx_file_path)
line=-1
itt=0
for row in data_frame.iterrows():
    line+=1
    
    if row[1]["done"]=="yes":
        pass
    try:
        driver.get(row[1]["url"])
        page_source = BeautifulSoup(driver.page_source)
        table=page_source.find('table',id='daily-results')
        
        tbody=table.find('tbody')
        tr=tbody.find_all('tr')

        for i in tr:
            itt+=1
            td=i.find_all('td')
            df.at[itt,"domain"]=td[0].getText()
            
            df.at[itt,"price"]=td[1].getText()
            df.at[itt,"venue"]=td[2].getText()
            df.at[itt,"date"]=page_source.find('time',class_='entry-date').getText()

            #for j in td:
                #print(j.getText())
    except:
        pass
    data_frame.at[line,"done"]="yes"
    print(df)
df.to_excel('test.xlsx', index=False)
data_frame.to_excel("1.xlsx", index=False)
print('saving')
        


