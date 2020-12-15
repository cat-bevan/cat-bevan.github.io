import math
import pandas as pd
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool

output_file('bokehGraph.html')

dateParser = lambda x: pd.datetime.strptime(x, '%Y %m %d')

def createDataFrames(givenMedia):
    dataframe = pd.read_csv(givenMedia + '.csv', delimiter = '|', parse_dates = ['publishDate'], date_parser = dateParser)
    dataframe = dataframe.set_index(['publishDate'])
    return dataframe

huffpostDF = createDataFrames('huffpostDF')
buzzfeedDF = createDataFrames('buzzfeedDF')
dailymailDF = createDataFrames('dailymailDF')
torontoStarDF = createDataFrames('torontoStarDF')
independentDF = createDataFrames('independentDF')

currDate = datetime(2008, 1, 1)

def createMonthlyDict(mediaSource):
    global currDate
    d = {}
    newList = []
    while currDate <= datetime.now():
        try:
            currDateStr = currDate.strftime('%Y-%m')
            fromDF = mediaSource.loc[currDateStr]
            addedHeadlines = fromDF['headlineText']
            d[currDateStr] = addedHeadlines
            newList.append(len(d[currDateStr]))
            currDate = currDate + relativedelta(months = 1)
        except:
            currDateStr = currDate.strftime('%Y-%m')
            d[currDateStr] = 'null'
            currDate = currDate + relativedelta(months = 1)
            newList.append(0)
    currDate = datetime(2008, 1, 1)
    return d, newList

huffpostDictList = createMonthlyDict(huffpostDF)
buzzfeedDictList = createMonthlyDict(buzzfeedDF)
dailymailDictList = createMonthlyDict(dailymailDF)
torontoStarDictList = createMonthlyDict(torontoStarDF)
independentDictList = createMonthlyDict(independentDF)

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
    months.append(currMonthStr)
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


    


