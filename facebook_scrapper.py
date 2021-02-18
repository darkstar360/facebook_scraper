from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import json
from decimal import Decimal
from datetime import datetime
import time
import csv

links=[]
with open('links.txt', newline='') as csv_file:
    rows = csv.reader(csv_file, delimiter=',', quotechar='|')
    for row in rows:
        links.append(row)
    csv_file.close()


data_lines =[]

option = Options()
driver = webdriver.Chrome(executable_path='chromedriver_win32/chromedriver.exe', options=option)
for link in links:
    # option.headless = True
    str = ''
    url = link[0]
    # url = url + '/about/'
    print('Getting url#{}'.format(url))
    driver.get(url + '/about')
    # time.sleep(6)
    page_source = BeautifulSoup(driver.page_source, 'lxml')

    element = page_source.find('meta', attrs={'property': "al:android:url"})
    val = element['content']
    profile_id_url = re.search(r'\d*\?', val)
    profile_id = profile_id_url.group(0).replace('?', '')
    print('profile ID#{}'.format(profile_id))
    str+= '\"' + profile_id + '\"' + ','
    try:
        element = driver.find_element_by_xpath("//a[@href =\"" + url + "/\"]")
        val = element.text
    except:
        val = 'No Full Name provided'
    print('Full Name# {}'.format(val))
    str += val + ','
    try:
        element = driver.find_element_by_xpath("//a[contains(@href, 'mailto:')]")
        val = element.text
    except:
        val = 'No Email Address provided'
    print('email# {}'.format(val))
    str += val + ','

    try:
        element = page_source.find('script', attrs={'type': 'application/ld+json'})
        val = json.loads(element.contents[0])['address']['addressLocality']
        val = json.loads(element.contents[0])['address']['addressLocality']
    except:
        val = 'No locality provided'
    element = page_source.find('script', attrs={'type': 'application/ld+json'})
    print('Location# {}'.format(val))
    str += '\"' + val + '\"' + '\n'
    data_lines.append(str)
with open('scraped_data.csv', 'a', newline='') as data_file:
    data_file.write('profile_id,Full_Name,Email,locality\n')
    data_file.writelines(data_lines)
    data_file.close()
driver.close()
