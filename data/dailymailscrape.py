import requests
from bs4 import BeautifulSoup as bs
import csv
from faker import Faker
import random

fake = Faker()

monthCount = 10
yearCount = 2020
dayCount = 18
numofLoops = 0


if len(str(monthCount)) == 1:
    monthLink = '0' + str(monthCount)
else:
    monthLink = str(monthCount)

def loopThrough():
    currCount = 1
    global monthCount
    global numofLoops

    if monthCount == 1:
        numofLoops = 31
    elif monthCount == 2:
        numofLoops = 28
    elif monthCount == 3:
        numofLoops = 31
    elif monthCount == 4:
        numofLoops = 30
    elif monthCount == 5:
        numofLoops = 31
    elif monthCount == 6:
        numofLoops = 30
    elif monthCount == 7:
        numofLoops = 31
    elif monthCount == 8:
        numofLoops = 31
    elif monthCount == 9:
        numofLoops = 30
    elif monthCount == 10:
        numofLoops = 31
    elif monthCount == 11:
        numofLoops = 30
    elif monthCount == 12:
        numofLoops = 31
        
    global dayCount
    global yearCount

    if len(str(monthCount)) == 1:
        monthLink = '0' + str(monthCount)
    else:
        monthLink = str(monthCount)


    while currCount <= numofLoops:
        dayCount = dayCount + 1
        headers = {'User-Agent': fake.user_agent()}
        
        if len(str(dayCount)) == 1:
            dayLink = '0' + str(dayCount)
        else:
            dayLink = str(dayCount)
            
        r = requests.get('https://www.dailymail.co.uk/home/sitemaparchive/day_' + str(yearCount) + monthLink + dayLink + '.html', headers=headers)

        soup = bs(r.content, 'html.parser')

        items =  soup.find_all('li', attrs={'class':'wogr2'})

        for item in items:
            with open('dailymail.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter = '|')
                writer.writerow(['Daily Mail', str(yearCount) + ' ' + monthLink + ' ' + dayLink, item.text])
        currCount = currCount + 1

    monthCount = monthCount + 1
    dayCount = 0
    if monthCount == 13:
        monthCount = 1
        yearCount = yearCount + 1

while True:
    loopThrough()
