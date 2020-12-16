import csv
#This script takes the full .csv files with upwards of 2 million headlines per news source, and scrapes them for trans-related headlines

currCSV = 'torontoStar.csv' #initialize current .csv to strip
destinationCSV = 'torontoStarDF.csv'
dateRange = ' ' #something optional I was playing with. Used this to extract those 2020-only .csv
currMedia = 'Toronto Star'

#all strings to search for are here. These were everything that came to mind for trans-related headlines. Very easy to re-purpose to any other set of words
searchStrings = ['transgender', 'transwoman', 'transman', 'tranny', 'trannie', 'transsexual', 'transexual', 'transperson', 'trans woman', 'trans man', 'trans person', 'transgendered', 'non-binary']

totalHeadlines = 0 #for calculating percentage of trans-related headlines
transHeadlines = 0
results = []

def rowCreate(csvFile): #extract by row
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
            totalHeadlines = totalHeadlines + 1
            currHeadline = row[2]
            correctHeadline = currHeadline.lower() #convert to lowercase to match to search strings
            for string in searchStrings:
                results.append(string in correctHeadline)
                output = any(results)
                if output == True: #check if there was any matches
                    transHeadlines = transHeadlines + 1
                    currDate = row[1]
                    output = False
                    results = []
                    printHeadline(currDate, currHeadline)

def printHeadline(currDate, currHeadline):
    with open(destinationCSV, 'a', newline = '') as file:
        writer = csv.writer(file, delimiter = '|')
        writer.writerow([currMedia, currDate, currHeadline])

def printTransPercentage():
    transPercentage = transHeadlines / totalHeadlines * 100
    print(transPercentage)

###############################################################################

currRows = rowCreate(currCSV)
currTransHeadlines = isolateTransHeadlines(currRows)
printTransPercentage
