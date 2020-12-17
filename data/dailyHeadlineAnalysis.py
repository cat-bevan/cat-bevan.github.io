import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

searchStrings = ['transgender', 'transwoman', 'transman', 'tranny', 'trannie', 'transsexual', 'transexual', 'transperson', 'trans woman', 'trans man', 'trans person', 'transgendered', 'non-binary', 'transwomen', 'transmen', 'trans women', 'trans men', 'transphobia']

results = []

currentDate = datetime.now()
toYesterday = currentDate - relativedelta(days = 1)
currDay = toYesterday.strftime('%d')
currMonth = toYesterday.strftime('%m')
currYear = toYesterday.strftime('%Y')
dateRange = currYear + ' ' + currMonth + ' ' + currDay

def rowCreate(csvFile):
    with open(csvFile, newline = '') as file:
        csvreader = csv.reader(file, delimiter = '|')
        rows = [row for row in csvreader]
        return rows

def isolateTransHeadlines(rows):
    global totalHeadlines
    global transHeadlines
    global results

    for row in rows:
        currDate = row[1]
        if currDate.find(dateRange) != -1:
            currHeadline = row[2]
            correctHeadline = currHeadline.lower()
            for string in searchStrings:
                results.append(string in correctHeadline)
                output = any(results)
                if output == True:
                    currDate = row[1]
                    output = False
                    results = []
                    printHeadline(currDate, currHeadline)

def printHeadline(currDate, currHeadline):
    with open(destinationCSV, 'a', newline = '') as file:
        writer = csv.writer(file, delimiter = '|')
        writer.writerow([currMedia, currDate, currHeadline])

###############################################################################
currCSV = 'torontoStar.csv'
destinationCSV = 'torontoStarDF.csv'
currMedia = 'Toronto Star'

currRows = rowCreate(currCSV)
currTransHeadlines = isolateTransHeadlines(currRows)

currCSV = 'dailymail.csv'
destinationCSV = 'dailymailDF.csv'
currMedia = 'Daily Mail'

currRows = rowCreate(currCSV)
currTransHeadlines = isolateTransHeadlines(currRows)

currCSV = 'huffpost.csv'
destinationCSV = 'huffpostDF.csv'
currMedia = 'HuffPost'

currRows = rowCreate(currCSV)
currTransHeadlines = isolateTransHeadlines(currRows)

currCSV = 'independent.csv'
destinationCSV = 'indendentDF.csv'
currMedia = 'The Independent'

currRows = rowCreate(currCSV)
currTransHeadlines = isolateTransHeadlines(currRows)
