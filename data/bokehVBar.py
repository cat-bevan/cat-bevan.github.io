#This script takes the full .csv's of trans-related headlines from each news source, sorts them by month,
#then visualizes them in an interactive way utilizing the bokeh module.

import math
import pandas as pd
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool

# essential imports. bokeh and pandas are third-party

output_file('bokehGraph.html')

dateParser = lambda x: pd.datetime.strptime(x, '%Y %m %d') #this is the date format I assigned while scraping my .csv files

def createDataFrames(givenMedia):
    dataframe = pd.read_csv(givenMedia + '.csv', delimiter = '|', parse_dates = ['publishDate'], date_parser = dateParser)
    dataframe = dataframe.set_index(['publishDate']) #allows for location via date, which will be important
    return dataframe

huffpostDF = createDataFrames('huffpostDF')
buzzfeedDF = createDataFrames('buzzfeedDF')
dailymailDF = createDataFrames('dailymailDF')
torontoStarDF = createDataFrames('torontoStarDF')
independentDF = createDataFrames('independentDF')

currDate = datetime(2008, 1, 1) #the date I chose to begin the chart. Where trans-related headlines began to appear with more frequency

def createMonthlyDict(mediaSource):
    global currDate
    d = {}
    newList = []
    while currDate <= datetime.now():
        try:
            currDateStr = currDate.strftime('%Y-%m')
            fromDF = mediaSource.loc[currDateStr] #finds every dataframe entry of the correct year and month I feed it
            addedHeadlines = fromDF['headlineText'] #extract headlines
            d[currDateStr] = addedHeadlines #add headlines to a dictionary, with the key as the month
            newList.append(len(d[currDateStr])) #to a list, add an integer equal to number of headlines in a given months
            currDate = currDate + relativedelta(months = 1) #forward by one month
        except: #occurs if no headlines are found for a given month
            currDateStr = currDate.strftime('%Y-%m')
            d[currDateStr] = 'null'
            currDate = currDate + relativedelta(months = 1)
            newList.append(0) #don't append with the filler text of 'null' - use 0 instead
    currDate = datetime(2008, 1, 1) #reset for the next news source
    return d, newList #returns the dictionary, and the list of ints

huffpostDictList = createMonthlyDict(huffpostDF)
buzzfeedDictList = createMonthlyDict(buzzfeedDF)
dailymailDictList = createMonthlyDict(dailymailDF)
torontoStarDictList = createMonthlyDict(torontoStarDF)
independentDictList = createMonthlyDict(independentDF)

#lists containing length values per month are here
huffpostFrequencyList = huffpostDictList[1]
buzzfeedFrequencyList = buzzfeedDictList[1]
dailymailFrequencyList = dailymailDictList[1]
torontoStarFrequencyList = torontoStarDictList[1]
independentFrequencyList = independentDictList[1]

huffpostFullDict = huffpostDictList[0]
buzzfeedFullDict = buzzfeedDictList[0]
dailymailFullDict = dailymailDictList[0]
torontoStarFullDict = torontoStarDictList[0]
independentFullDict = independentDictList[0]

#creates list containing large strings of included headlines, one value per month
huffpostHeadlinesList = list(huffpostFullDict.values())
buzzfeedHeadlinesList = list(buzzfeedFullDict.values())
dailymailHeadlinesList = list(dailymailFullDict.values())
torontoStarHeadlinesList = list(torontoStarFullDict.values())
independentHeadlinesList = list(independentFullDict.values())

currMonth = datetime(2008, 1, 1)
months = []
newsOutlets = ['Huffpost', 'Buzzfeed', 'Daily Mail', 'Toronto Star', 'The Independent']
colours = ['#ADC18C', 'purple', 'orange', 'blue', 'red']

while currMonth <= datetime.now():

    currMonthStr = currMonth.strftime('%Y-%m')
    months.append(currMonthStr) #set length of chart to grow to current date
    currMonth = currMonth + relativedelta(months = 1)


plottingData = {'months': months,
        'Huffpost' : huffpostFrequencyList, 
        'Buzzfeed' : buzzfeedFrequencyList,
        'Daily Mail' : dailymailFrequencyList,
        'Toronto Star' : torontoStarFrequencyList,
        'The Independent' : independentFrequencyList,
        'HuffpostHeadlines' : huffpostHeadlinesList,
        'BuzzfeedHeadlines' : buzzfeedHeadlinesList,
        'DailymailHeadlines' : dailymailHeadlinesList,
        'TorontoStarHeadlines' : torontoStarHeadlinesList,
        'IndependentHeadlines' : independentHeadlinesList}

source = ColumnDataSource(data=plottingData)

p = figure(x_range = months,
        plot_height = 800,
        plot_width = 3000,
        title = 'Trans-related stories from 2008 to the present day')

renderers = p.vbar_stack(newsOutlets, x = 'months', width = 0.9, color = colours, source = source, legend_label = newsOutlets, name = newsOutlets)

#had to write custom tooltips for each news source so that the tooltips carry each's own headlines. Custom HTML also allows for spacing and font alteration
customHuffpostTooltips = """ 
    <div>
        <div>
            $name @months: @$name trans-related headlines;
        </div>
        <div>
            <div style="font-size: 10px; width: 500px;">@HuffpostHeadlines</div>
        </div>
    </div>
"""
customBuzzfeedTooltips = """
    <div>
        <div>
            $name @months: @$name trans-related headlines;
        </div>
        <div>
            <div style="font-size: 10px; width: 500px">@BuzzfeedHeadlines</div>
        </div>
    </div>
"""
customDailyMailTooltips = """
    <div>
        <div>
            $name @months: @$name trans-related headlines;
        </div>
        <div>
            <div style="font-size: 10px; width: 500px;">@DailymailHeadlines</div>
        </div>
    </div>
"""
customTorontoStarTooltips = """
    <div>
        <div>
            $name @months: @$name trans-related headlines;
        </div>
        <div>
            <div style="font-size: 10px; width: 500px;">@TorontoStarHeadlines</div>
        </div>
    </div>
"""
customIndependentTooltips = """
    <div>
        <div>
            $name @months: @$name trans-related headlines;
        </div>
        <div>
            <div style="font-size: 10px; width: 500px;">@IndependentHeadlines</div>
        </div>
    </div>
"""


for r in renderers:
    if r.name == 'Huffpost':
        hover = HoverTool(tooltips = customHuffpostTooltips, renderers = [r])
    elif r.name == 'Buzzfeed':
        hover = HoverTool(tooltips = customBuzzfeedTooltips, renderers = [r])
    elif r.name == 'Daily Mail':
        hover = HoverTool(tooltips = customDailyMailTooltips, renderers = [r])
    elif r.name == 'Toronto Star':
        hover = HoverTool(tooltips = customTorontoStarTooltips, renderers = [r])
    elif r.name == 'The Independent':
        hover = HoverTool(tooltips = customIndependentTooltips, renderers = [r])
    p.add_tools(hover)
        
p.y_range.start = 0
p.x_range.range_padding = 0
p.xgrid.grid_line_color = None
p.xaxis.major_label_orientation = math.pi/2
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = 'top_left'
p.legend.orientation = 'horizontal'

show(p)


    


