import csv
currCSV = 'torontoStar.csv'
destinationCSV = 'torontoStarDF.csv'
dateRange = ' '
currMedia = 'Toronto Star'

searchStrings = ['transgender', 'transwoman', 'transman', 'tranny', 'trannie', 'transsexual', 'transexual', 'transperson', 'trans woman', 'trans man', 'trans person', 'transgendered', 'non-binary']

totalHeadlines = 0
transHeadlines = 0
results = []

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
            totalHeadlines = totalHeadlines + 1
            currHeadline = row[2]
            correctHeadline = currHeadline.lower()
            for string in searchStrings:
                results.append(string in correctHeadline)
                output = any(results)
                if output == True:
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
