import requests
from bs4 import BeautifulSoup as bs
import csv
from faker import Faker
import random

#necessary imports. Faker, bs4, and requests are third-party
#do note that I wrote my scrape scripts like this one a couple of months before the rest of the scripts. My Python is certainly messier here
fake = Faker()

monthCount = 10 #initialize what date you want to start scraping the website from
yearCount = 2020
dayCount = 17
numofLoops = 0

# this messy section here was written before I was aware of datetime objects in Python

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
        headers = {'User-Agent': fake.user_agent()} #random user-agent to bypass website defensives against webscraping
        
        if len(str(dayCount)) == 1:
            dayLink = '0' + str(dayCount)
        else:
            dayLink = str(dayCount)
        # these scrape scripts work by looping through all possible days in a url which is structured like below
        # digital archives which organize their daily headlines by one page per day is ideal, like this
        r = requests.get('https://www.huffpost.com/archive/' + str(yearCount) + '-' + monthLink + '-' + dayLink, headers=headers)

        soup = bs(r.content, 'html.parser')

        items =  soup.find_all('div', attrs={'class':'card__headline__text'}) #this changes from website to website

        for item in items:
            with open('huffpost.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter = '|')
                writer.writerow(['Huffpost', str(yearCount) + ' ' + monthLink + ' ' + dayLink, item.text])
        currCount = currCount + 1

    monthCount = monthCount + 1
    dayCount = 0
    if monthCount == 13:
        monthCount = 1
        yearCount = yearCount + 1

while True:
    loopThrough()
