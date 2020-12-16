import math
import pandas as pd
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool

output_file('bokeh30days.html')

dateParser = lambda x: pd.datetime.strptime(x, '%Y %m %d')

def createDataFrames(givenMedia):
    dataframe = pd.read_csv(givenMedia + '.csv', delimiter = '|', parse_dates = ['publishDate'], date_parser = dateParser)
    dataframe = dataframe.set_index(['publishDate'])
    return dataframe

huffpostDF = createDataFrames('huffpostDF')
dailymailDF = createDataFrames('dailymailDF')
torontoStarDF = createDataFrames('torontoStarDF')
independentDF = createDataFrames('independentDF')

currDate = datetime.now() - relativedelta(days = 30)

def createDailyDict(mediaSource):
    global currDate
    d= {}
    newList = []
    while currDate <= datetime.now():
        try:
            currDateStr = currDate.strftime('%Y-%m-%d')
            fromDF = mediaSource.loc[currDateStr]
            addedHeadlines = fromDF['headlineText']
            d[currDateStr] = addedHeadlines
            if isinstance(d[currDateStr], str):
                newList.append(1)
            else:
                newList.append(len(d[currDateStr]))
            currDate = currDate + relativedelta(days = 1)
        except:
            currDateStr = currDate.strftime('%Y-%m-%d')
            d[currDateStr] = 'null'
            currDate = currDate + relativedelta(days = 1)
            newList.append(0)
    currDate = datetime.now() - relativedelta(days = 30)
    return d, newList

huffpostDictList = createDailyDict(huffpostDF)
dailymailDictList = createDailyDict(dailymailDF)
torontoStarDictList = createDailyDict(torontoStarDF)
independentDictList = createDailyDict(independentDF)

huffpostFrequencyList = huffpostDictList[1]
dailymailFrequencyList = dailymailDictList[1]
torontoStarFrequencyList = torontoStarDictList[1]
independentFrequencyList = independentDictList[1]

huffpostFullDict = huffpostDictList[0]
dailymailFullDict = dailymailDictList[0]
torontoStarFullDict = torontoStarDictList[0]
independentFullDict = independentDictList[0]

huffpostHeadlinesList = list(huffpostFullDict.values())
dailymailHeadlinesList = list(dailymailFullDict.values())
torontoStarHeadlinesList = list(torontoStarFullDict.values())
independentHeadlinesList = list(independentFullDict.values())

currDay = datetime.now() - relativedelta(days = 30)
days = []
newsOutlets = ['Huffpost', 'Daily Mail', 'Toronto Star', 'The Independent']
colours = ['#ADC18C', 'orange', 'blue', 'red']

while currDay <= datetime.now():
    currDayStr = currDay.strftime('%Y-%m-%d')
    days.append(currDayStr)
    currDay = currDay + relativedelta(days = 1)

plottingData = {'days': days,
        'Huffpost' : huffpostFrequencyList,
        'Daily Mail' : dailymailFrequencyList,
        'Toronto Star' : torontoStarFrequencyList,
        'The Independent' : independentFrequencyList,
        'HuffpostHeadlines' : huffpostHeadlinesList,
        'DailymailHeadlines' : dailymailHeadlinesList,
        'TorontoStarHeadlines' : torontoStarHeadlinesList,
        'IndependentHeadlines' : independentHeadlinesList}

source = ColumnDataSource(data = plottingData)

p = figure(x_range = days,
        plot_height = 500,
        plot_width = 900,
        title = 'Trans-related stories over the past 30 days')

renderers = p.vbar_stack(newsOutlets, x = 'days', width = 0.9, color = colours, source = source, legend_label = newsOutlets, name = newsOutlets)

customHuffpostTooltips = """
    <div>
        <div>
            $name @days: @$name trans-related headlines;
        </div>
        <div>
            <div style="font-size: 10px; width: 400px;">@HuffpostHeadlines</div>
        </div>
    </div>
"""
customDailyMailTooltips = """
    <div>
        <div>
            $name @days: @$name trans-related headlines;
        </div>
        <div>
            <div style="font-size: 10px; width: 400px;">@DailymailHeadlines</div>
        </div>
    </div>
"""
customTorontoStarTooltips = """
    <div>
        <div>
            $name @days: @$name trans-related headlines;
        </div>
        <div>
            <div style="font-size: 10px; width: 400px;">@TorontoStarHeadlines</div>
        </div>
    </div>
"""
customIndependentTooltips = """
    <div>
        <div>
            $name @days: @$name trans-related headlines;
        </div>
        <div>
            <div style="font-size: 10px; width: 400px;">@IndependentHeadlines</div>
        </div>
    </div>
"""

for r in renderers:
    if r.name == 'Huffpost':
        hover = HoverTool(tooltips = customHuffpostTooltips, renderers = [r])
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
