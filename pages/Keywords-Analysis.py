import dash
from dash import html, dcc, callback, Input, Output, ctx
import operator
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io
import os

#import data-------------------------------------------------------------------

buffer = io.StringIO()

# list of data
files_name = [file_name for file_name in os.listdir() if '.json' in file_name]

def readfichier():
    with open('./data.txt', 'r') as file:
        fichier = file.read().rstrip()
    return fichier

def open_data():
    file_name = readfichier()
    # open and load file
    f = open(file_name, 'r', encoding='utf-8')
    data = json.loads(f.read())
    f.close()
    return data

global data
data = open_data()

dash.register_page(__name__)

def updateDropdown():

    k_years = []
    for keys in sorted(data["metadata-all"]["fr"]["year"].keys(), key=int, reverse=True):
        k_years.append(keys)
    return k_years


options = updateDropdown()

layout = html.Div([
    html.H1('Keywords Analysis'),
    html.Div([
    dcc.Dropdown(
        id="dropdown",
        options= options,
        value= options[0],
        clearable=False,
    ),
    dcc.Graph(id="graphhaut",clickData=None,hoverData=None,style={'width': '100%','height':'50%', 'display': 'inline-block'})],id="fig1",),
    html.Div([
    dcc.Graph(id="graphbas",style={'width': '40%','height':'50vh', 'display': 'inline-block'}),
    dcc.Graph(id="graphbas2",style={'width': '60%','height':'50vh', 'display': 'inline-block'})
    ],id="fig2"),
],id="div_global")


@callback(
    Output("graphhaut", "figure"),
    Output("dropdown","options"), 
    Input("graphhaut", "clickData"),
    Input("dropdown", "value"))
def update_bar_chart(clickData, year):

    dd = updateDropdown()
    if ctx.triggered_id == "dropdown":
        clickData = None
        fig = createBarChart(year, None)
        return fig, dd
    elif clickData is None:
        clickData = None
        global data
        data = open_data()
        fig = createBarChart(year, None)
        return fig, dd
    else:
        index = clickData["points"][0]["pointNumber"]
        fig = createBarChart(year, index)
        return fig, dd

def createBarChart(year, index):

    day = []
    values = []
    lcolor=[]
    data_day = data["metadata-all"]["fr"]["day"][year]

    data_month_sorted = sorted(data_day.keys(),key=int)
    for i in data_month_sorted:
        data_day_sorted = sorted(data_day[str(i)],key=int)

        for keys in data_day_sorted:
            day_str = str(keys) + "/" + str(i) + "/" + str(year)
            day.append(day_str)
            values.append(data_day[str(i)][keys]["num"])
            if len(lcolor) == index:
                lcolor.append('rgba(222,45,38,0.8)')
            else:
                lcolor.append('rgba(149,177,209,1)')


    df = pd.DataFrame(values,index=day,columns=["nb_articles"])

    fig = go.Figure(data=[go.Bar(x= df.index.values, y=df['nb_articles'], marker=dict(color = lcolor))])
    fig.update_layout(title_text='Number of articles per day',title_x=0.5, font=dict(family="Courier New, Monospace"))

    return fig

#------------------------------------------------------------------------------------------------------------


@callback(
    Output(component_id="graphbas", component_property="figure"),
    Input('graphhaut', 'clickData'),
    Input('graphbas', 'clickData'),
    Input('dropdown', 'value'))
def update_bar_chart2(clickData,clickData2,value):
    
    if clickData is None or ctx.triggered_id == "dropdown":
        return go.Figure(data=[go.Bar()]).update_layout(title_text='Most Keywords in a day',title_x=0.5, font=dict(family="Courier New, Monospace"))
    
    if ctx.triggered_id == "graphhaut" :
        clickData2 = None
        fig2 = createBarChart2(clickData,clickData2)
        return fig2
    if ctx.triggered_id == "graphbas" :
        fig2 = createBarChart2(clickData,clickData2)
        return fig2

def createBarChart2(clickData,clickData2):

    s = str(clickData["points"][0]["x"])
    date = s.split("/")
    data_day = data["metadata-all"]["fr"]["day"][str(date[2])][str(date[1])][str(date[0])]

    kwsSort = dict(sorted(data_day["kws"].items(), key=operator.itemgetter(1), reverse=True)[:5])
    df = pd.DataFrame.from_dict(kwsSort, orient='index',columns=['Number'])
    
    index = None
    if clickData2 != None:
        index = clickData2["points"][0]["pointNumber"]

    lcolor = []
    for i in range(0,5):
        if len(lcolor) == index:
            lcolor.append('rgba(222,45,38,0.8)')
        else:
            lcolor.append('rgba(0,102,204,1)')

    fig2 = go.Figure(data=[go.Bar(x=df['Number'], y=df.index.values, orientation='h', marker = dict(color = lcolor))])
    fig2.update_layout(title_text='Most Keywords in a day',title_x=0.5, font=dict(family="Courier New, Monospace"))
    return fig2

#----------------------------------------------------------------------------------------------------------------------------------------------------

def getFrequencyKW(keyword,year):
    NbKeywork = []
    days = []
    data_day = data["metadata-all"]["fr"]["day"][year]
    data_month_sorted = sorted(data_day.keys(),key=int)

    for i in data_month_sorted:
        data_day_sorted = sorted(data_day[str(i)],key=int)
        for j in data_day_sorted:

            if keyword in list(data_day[str(i)][str(j)]["kws"].keys()):
                NbKeywork.append(int(data_day[str(i)][str(j)]["kws"][str(keyword)]))
                days.append(str(j) + "/" + str(i) + "/" + str(year))

    return NbKeywork, days


def getAllDays(year):

    data_day = data["metadata-all"]["fr"]["day"][year]
    data_month_sorted = sorted(data_day.keys(),key=int)
    days = []

    for i in data_month_sorted:
        data_day_sorted = sorted(data_day[str(i)],key=int)
        for j in data_day_sorted:
            days.append(str(j) + "/" + str(i) + "/" + str(year))

    return days

def createLineChart(date,index):
    kwsSort={}
    data_day = data["metadata-all"]["fr"]["day"][str(date[2])][str(date[1])][str(date[0])]
    
    if index != None:
        dico = dict(sorted(data_day["kws"].items(), key=operator.itemgetter(1), reverse=True)[:5])
        kwsSort = dict([list(dico.items())[index]])
    else:
        kwsSort = dict(sorted(data_day["kws"].items(), key=operator.itemgetter(1), reverse=True)[:5])

    liste = getAllDays(str(date[2]))
    dict_frequency =  {}

    for i in range(len(list(kwsSort))):
        values = getFrequencyKW(list(kwsSort.keys())[i],str(date[2]))

        list_frequency = values[0]
        list_dates = values[1]
        real_frequency = []

        for x in liste:

            if x in list_dates:
                index = list_dates.index(x)
                real_frequency.append(list_frequency[index])
            else:
                 real_frequency.append(0)

        dict_frequency[list(kwsSort.keys())[i]] = real_frequency
    
    df = pd.DataFrame(data=dict_frequency,index=liste)

    fig = px.line(df, x=df.index.values, y=df.columns, markers=True) 
    fig.update_layout(title_text='Frequency of Keywords in a year',title_x=0.5, font=dict(family="Courier New, Monospace"))
    return fig


@callback(
    Output(component_id="graphbas2", component_property="figure"),
    Input('graphhaut', 'clickData'),
    Input('graphbas','clickData'),
    Input('dropdown', 'value'))
def update_line_chart(clickData,clickData2,value):
    if clickData is None or ctx.triggered_id == "dropdown":
        return px.line().update_layout(title_text='Frequency of Keywords in a year',title_x=0.5, font=dict(family="Courier New, Monospace"))

    s = str(clickData["points"][0]["x"])
    date = s.split("/")
    index = None

    if ctx.triggered_id == "graphhaut" :
        fig = createLineChart(date,None)
        return fig

    if ctx.triggered_id == "graphbas" :
        index = clickData2["points"][0]["pointNumber"]
        fig = createLineChart(date,index)
        return fig

