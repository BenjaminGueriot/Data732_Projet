import dash
from dash import html, dcc, callback, Input, Output, dash_table, ctx
import operator
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io
import os
from urllib.request import urlopen
import json
from geopy.geocoders import Nominatim
import csv
import time
import dash_bootstrap_components as dbc

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


all_countries = []

with open('pays.csv', 'rt') as f:
     reader = csv.reader(f, delimiter=',')
     for row in reader:
        all_countries.append(row[4])
        all_countries.append(row[5])
   

dash.register_page(__name__)


loaded = False

current_state = "Loading"



def getPosFromCountry(countries):
    global all_lat
    all_lat = []
    global all_lon
    all_lon = []
    global countries_placed
    countries_placed = []

    countries_list = []
    
    for country in countries:
        
        if country in all_countries:
            countries_placed.append(str(country))

            geolocator = Nominatim(user_agent="app")
            try:
                location = geolocator.geocode(str(country))

                if location:
                    lat = location.latitude
                    lon = location.longitude
                    
                    value = data["metadata-all"]["fr"]["all"]["loc"][str(country)]
                    all_lat.append(lat)
                    all_lon.append(lon)
                    pos = [country, value, lon, lat]

                    countries_list.append(pos)
            except:
                pass

            
    global loaded
    loaded = True

    return countries_list

df1 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

def get_layout():
    return  html.Div([
    html.H1('Countries Analysis'),
    dcc.Interval(id='interval', interval=1000, n_intervals=0),
    html.H1(id='label1', children='', style={'text-align' : 'center'}),
    html.Div([
        
        dcc.Graph(id="map", figure=px.scatter_geo(projection="natural earth").update_layout(title_text='World map of countries being called',title_x=0.5,title_y=0.8, font=dict(family="Courier New, Monospace")),style={'width': '50%','height':'100vh', 'display': 'inline-block'})
,
        html.Div([

            dcc.Graph(id="results",style={'width': '100%','height':'100%', 'display': 'flex'}),         


           
        ], style={'width': '50%','height':'100vh', 'display': 'inline-block'}),

        dash_table.DataTable(
                id='table',
                style_cell={'textAlign': 'left'},
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'width':'auto'
                },
                columns=[
                dict(id='title', name='Title'),
                dict(id='description', name='Description'),
                ],
                data=[dict(title='testas', description='te')],
            ),
       
        ]),
    ],id="div_global")

layout = get_layout()

@callback(
    Output('label1', 'children'),
    Input('interval', 'n_intervals'))
def update_interval(n):
    
    global current_state
    global loaded

    if loaded == True:
        return ""
    else:
        if current_state == "Loading":
            current_state = "Loading ."
        elif current_state == "Loading .":
            current_state =  "Loading . ."
        elif current_state == "Loading . .":
            current_state = "Loading . . ."
        elif current_state == "Loading . . .":
            current_state = "Loading"""

    return current_state

@callback(
    Output("map", "figure"),
    Input("map","figure"))
def update_map(clickData):
    
    global data
    data = open_data()

    global loaded
    loaded = False

    data_countries = data["metadata-all"]["fr"]["all"]["loc"].keys()

    rows = getPosFromCountry(data_countries)

    '''rows=[['501-600','15','16.3700359','-2.2900239'],
      ['till 500','4','12.5','27.5'],
      ['more 1001','41','-115.53333','38.08'],
      ]'''

    colmns=['Pays','data','longitude','latitude']
    df=pd.DataFrame(data=rows, columns=colmns)
    df = df.astype({"data": int})

    fig=px.scatter_geo(df,lon='longitude', lat='latitude',
                      color='Pays',
                      opacity=0.5,
                      size='data',
                      projection="natural earth", hover_data={'longitude':False,'latitude':False,'data':False})

    fig.add_trace(go.Scattergeo(lon=df["longitude"],
              lat=df["latitude"],
              text=df["data"],
              textposition="middle center",
              mode='text',
              showlegend=False))
    

    fig = fig.update_layout(title_text='World map of countries being called',title_x=0.5,title_y=0.8, font=dict(family="Courier New, Monospace"))
    
    return fig

#-------------------------------------------------------------------------------



def createBarChart(country): 
        global list_titles
        list_titles = dict()
        global list_titles_todescription
        list_titles_todescription = dict()

        dico_presence = dict()


        for year in data["data-all"].keys():

            data_day = data["data-all"][year]

            data_month_sorted = sorted(data_day.keys(),key=int)

            for i in data_month_sorted:
                data_day_sorted = sorted(data_day[str(i)],key=int)

                for keys in data_day_sorted:

                    day_str = str(keys) + "/" + str(i) + "/" + str(year)

        


                    table = data["data-all"][year][str(i)][keys]

                    for j in range(len(table)):
        

                            title = data["data-all"][year][str(i)][keys][j]['title']
                            description = data["data-all"][year][str(i)][keys][j]['description']

                            dico_countries = data["data-all"][year][str(i)][keys][j]['loc']

                            if country in dico_countries:

                                value = dico_countries[country]
                                list_titles_todescription[title] = description
                                list_titles[title] = value
                                dico_presence[day_str] = value

                            
        return dico_presence

@callback(
    Output("results", "figure"),
    Input("map","clickData"),
    Input("results","clickData"))
def update__bar_chart(clickData, clickData2):

    fig = go.Figure().update_layout(title_text='Most times a country is called per article',title_x=0.5, font=dict(family="Courier New, Monospace"))

    if ctx.triggered_id == "map" : 
         clickData2 = None
 
    if clickData != None:

        lon = clickData['points'][0]['lon']
        
        if lon in all_lon:
            
            ind = all_lon.index(lon)

            country = countries_placed[ind]

            dico = createBarChart(country)


            dicoSort = dict(sorted(dico.items(), key=operator.itemgetter(1), reverse=True)[:5])

            index = None
            if clickData2 != None:
                index = clickData2["points"][0]["pointNumber"]

            lcolor = []
            for i in range(0,5):
                if len(lcolor) == index:
                    lcolor.append('rgba(222,45,38,0.8)')
                else:
                    lcolor.append('rgba(0,102,204,1)')

            df = pd.DataFrame.from_dict(dicoSort, orient='index',columns=['Number'])
            fig = go.Figure(data=[go.Bar(x=df['Number'], y=df.index.values, orientation='h', marker = dict(color = lcolor))])
            fig.update_layout(title_text='Most times ' + str(country) + ' is called per article',title_x=0.5, font=dict(family="Courier New, Monospace"))
        
    return fig

@callback(
    Output("table", "data"),
    Input("results","clickData"),
    Input("map","clickData"))
def show_infos(clickData, clickData2):

    if ctx.triggered_id != "map" : 

        if clickData != None:

            dico = list_titles
            dicoSort = dict(sorted(dico.items(), key=operator.itemgetter(1), reverse=True)[:5])

            titles = list(dicoSort.keys())

            index = clickData['points'][0]['pointIndex']

            descriptions = list_titles_todescription[titles[index]]

            return [dict(title=titles[index], description=descriptions)]

    return [dict(title='TBD', description='TBD')]
