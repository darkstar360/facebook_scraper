from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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
        links.append(row[0])
    csv_file.close()

option = Options()
option.add_argument('--incognito')
driver = webdriver.Chrome(executable_path='chromedriver_win32/chromedriver.exe', options=option)

followers = []
for link in links:
    # driver.get('chrome://settings/clearBrowserData')
    # driver.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)
    # time.sleep(2)
    # driver.find_element_by_id('clearBrowsingDataConfirm').click()
    # time.sleep(5)
    try:
        driver.get(link)
        i = 0
        try:
            driver.find_element_by_xpath('//button[@title="Accept All"]').click()
        except Exception as e:
            print('Exception#{}'.format(e))
        while i<10:
            try:
                driver.find_element_by_id('expanding_cta_close_button').click()
            except:
                pass
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)
            i+=1
        # time.sleep(5)
        # driver.find_element_by_xpath('//a[@class="_7a99 _21q1 _p"]').click()
        time.sleep(5)

        page_source = BeautifulSoup(driver.page_source)
        ppls = []
        ppl_url = page_source.find_all('a', attrs={'class': '_6qw4'})
        for ppl in ppl_url:
            val = ppl['href']
            val = re.search('(\w||\.||-\d)*\?', val).group(0).replace('?', '')
            ppls.append('https://www.facebook.com/'+val)
    except Exception as  e:
        print('Exception#{}'.format(e))

data_lines =[]
# ppls = ['https://www.facebook.com/sudhanaidu9619']

while True:
    try:
        ppls.remove('https://www.facebook.com/')
    except:
        break

for link in set(ppls):
    # option.headless = True
    try:
        str = ''
        url = link
        # url = url + '/about/'
        print('Getting url#{}'.format(url))
        driver.get(url + '/about')
        time.sleep(6)
        page_source = BeautifulSoup(driver.page_source, 'lxml')

        element = page_source.find('meta', attrs={'property': "al:android:url"})
        val = element['content']
        profile_id_url = re.search(r'profile/([0-9])*', val)
        profile_id = profile_id_url.group(0).replace('profile/', '')
        print('profile ID#{}'.format(profile_id))
        str+= '\"' + profile_id + '\"' + ','
        try:
            # element = page_source.find('meta', attrs={'property': "og:description"})
            element = driver.find_element_by_xpath('//a[@class="_2nlw _2nlv"]')
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
    except Exception as e:
        print('Exception#{}'.format(e))
with open('scraped_data.csv', 'a', newline='') as data_file:
    data_file.write('profile_id,Full_Name,Email,locality\n')
    data_file.writelines(data_lines)
    data_file.close()
driver.close()