import requests
from bs4 import BeautifulSoup as bs
import csv
from faker import Faker
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

fake = Faker()

headers = {'User-Agent': fake.user_agent()}

currTime = datetime.now()
toYesterday = currTime - relativedelta(days = 1)
daytoScrape = toYesterday.strftime('%d')
monthtoScrape = toYesterday.strftime('%m')
yeartoScrape = toYesterday.strftime('%Y')
        
r = requests.get('https://www.dailymail.co.uk/home/sitemaparchive/day_' + yeartoScrape + monthtoScrape + daytoScrape + '.html', headers=headers)

soup = bs(r.content, 'html.parser')

items =  soup.find_all('li', attrs={'class':'wogr2'})

for item in items:
    with open('dailymail.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter = '|')
        writer.writerow(['Daily Mail', yeartoScrape + ' ' + monthtoScrape + ' ' + daytoScrape, item.text])

r = requests.get('https://www.huffpost.com/archive/' + yeartoScrape + '-' + monthtoScrape + '-' + daytoScrape, headers=headers)

soup = bs(r.content, 'html.parser')

items =  soup.find_all('div', attrs={'class':'card__headline__text'})

for item in items:
    with open('huffpost.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter = '|')
        writer.writerow(['Huffpost', yeartoScrape + ' ' + monthtoScrape + ' ' + daytoScrape, item.text])

r = requests.get('https://www.independent.co.uk/archive/' + yeartoScrape + '-' + monthtoScrape + '-' + daytoScrape, headers=headers)

soup = bs(r.content, 'html.parser')

items =  soup.find_all('a', attrs={'class':'sc-qOtIQ ioiXLw'})

for item in items:
    with open('independent.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter = '|')
        writer.writerow(['The Independent', yeartoScrape + ' ' + monthtoScrape + ' ' + daytoScrape, item.text])
        
r = requests.get('https://www.thestar.com/archive/' + yeartoScrape + '/' + monthtoScrape + '/' + daytoScrape + '.html')

soup = bs(r.content, 'html.parser')

items =  soup.find_all('a', attrs={'class':'text-block__link'})

for item in items:
    with open('torontoStar.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter = '|')
        writer.writerow(['Toronto Star', yeartoScrape + ' ' + monthtoScrape + ' ' + daytoScrape, item.text])

