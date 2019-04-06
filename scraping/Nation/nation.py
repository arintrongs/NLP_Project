from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import csv
driver = webdriver.Chrome(
    '/Users/eqsk134/Documents/Datasci_indiv/Mild/chromedriver')

from urllib.parse import urlparse
from datetime import date
import dateparser
import datetime


def get_page(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    mainpage = response.read().decode('utf-8')
    return mainpage


import pandas as pd
df = pd.DataFrame(columns=['headline', 'date', 'DOW', 'time', 'view',
                           'like', 'share', 'comment', 'category', 'tag', 'content'])
df_nocon = pd.DataFrame(columns=['headline', 'date', 'DOW',
                                 'time', 'view', 'like', 'share', 'comment', 'category', 'tag'])
index = 378700064
idx = 0
url = "http://www.nationtv.tv/main/content/"
month = {"มกราคม": '01', "กุมภาพันธ์": '02', "มีนาคม": '03', "เมษายน": '04', "พฤษภาคม": '05', "มิถุนายน": '06',
         "กรกฎาคม": '07', "สิงหาคม": '08', "กันยายน": '09', "ตุลาคม": '10', "พฤศจิกายน": '11', "ธันวาคม": '12'}
month_num = {"มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
             "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12}
day_in_week = {0: 'MON', 1: 'TUE', 2: 'WED',
               3: 'THU', 4: 'FRI', 5: 'SAT', 6: 'SUN'}

for i in range(1000):
    page_source = get_page(url + str(index))
    driver.get(url + str(index))
    index -= 1
    if (driver.current_url == "http://www.nationtv.tv/main/"):
        print('skip')
        continue
    secondpage_parser = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        for a in secondpage_parser.findAll(True, {'class': ['breadcrumb']}):
            category = a.find_all('a')[2].get_text()
            headline = a.find_all('a')[-1].get_text()
        print(headline)
        temp_date = secondpage_parser.findAll(
            True, {'class': ['date']})[0].get_text()
        temp_date = temp_date.split()
        time = temp_date[-1]
        date = ""
        date += temp_date[0]
        if len(date) == 1:
            date = "0"+date
        date += "/"+str(month[temp_date[1]])+"/"+temp_date[2]
        view = secondpage_parser.find(
            True, {'id': ['viewCountDisplay']}).get_text()
        DOW = day_in_week[datetime.datetime(
            int(temp_date[2])-543, month_num[temp_date[1]], int(temp_date[0])).weekday()]
        share = secondpage_parser.find(
            True, {'id': ['shareCountDisplay']}).get_text()
        content = ""
        for elm in secondpage_parser.find(True, {'id': ['the-post']}).find_all('p', class_=""):
            content += elm.get_text()
        df_nocon.loc[idx] = [headline, date, DOW,
                             time, view, "", share, "", category, ""]
        df.loc[idx] = [headline, date, DOW, time,
                       view, "", share, "", category, "", content]
        idx += 1
    except:
        print("bug")
df.to_csv('nation_news_4.csv')
df_nocon.to_csv('nation_news_nocon_4.csv')
