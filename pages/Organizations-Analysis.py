import operator
import dash
from dash import html, dcc, callback, Input, Output, ctx, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io
import os
import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('fr')

files_name = [file_name for file_name in os.listdir() if '.json' in file_name]
# name of the lightest file

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

#-------------------------------------------------------------------------------

dash.register_page(__name__)


def create_org_bar_chart():
    
    global data
    data = open_data()

    data2 = data["metadata-all"]["fr"]["month"]
    all_org_dict = dict(sorted(data["metadata-all"]["fr"]["all"]["org"].items(), key=operator.itemgetter(1), reverse=True)[:15])
    all_org = []
    for keys in list(all_org_dict.keys()):
        all_org.append(keys)
        
    global dict_frequency
    dict_frequency={}
    count = 0

    for org in all_org:
        
        data_year_sorted = sorted(data2.keys(),key=int)
        
        for i in data_year_sorted:
            data_month_sorted = sorted(data2[str(i)].keys(),key=int)
            for j in data_month_sorted:
                real_frequency = []
                month = str(j) + "/" + str(i)
            
                real_frequency.append(str(org))
                real_frequency.append(month)

                if org in list(data2[str(i)][str(j)]["org"].keys()):
                    real_frequency.append(data2[str(i)][str(j)]["org"][str(org)])
                else:
                    real_frequency.append(0)

                dict_frequency[str(count)] = real_frequency
                count += 1
     
    df = pd.DataFrame.from_dict(dict_frequency,orient = 'index',columns=["org","month","value"])

    fig = px.bar(df,x=df["value"], y=df["org"], range_x=[0,df["value"].max()], orientation='h', animation_frame=df["month"], animation_group=df["org"])
    fig.update_layout(title_text='Most Organizations per month',title_x=0.5)
    return fig

def get_all_month():

    all_month =[]

    data2 = data["metadata-all"]["fr"]["month"]

    data_year_sorted = sorted(data2.keys(),key=int)
    for i in data_year_sorted:
        data_month_sorted = sorted(data2[str(i)].keys(),key=int)
        for j in data_month_sorted:
            month = str(j) + "/" + str(i)
            all_month.append(month)

    return all_month

layout = html.Div([
    html.H1('Organization Analysis'),
    html.Div([
    dcc.Graph(id="graph1",style={'width': '100%','height':'50vh', 'display': 'inline-block'})
    ],id="fig1"),
    html.Div([
    html.Div(dcc.Graph(id="graph2"),style={'width': '50%','height':'50vh', 'display': 'inline-block'}),
    html.Div(dash_table.DataTable(
                id='table_org',
                style_cell={'textAlign': 'center'},
                style_data={
                    'whiteSpace': 'normal',
                    'height': '50vh',
                    'width':'auto',
                },
                style_table={
                'maxHeight': '53vh',
                'width': '100%',
                'minWidth': '100%',
                'overflowY': 'scroll',
                },
                columns=[
                dict(id='organization', name='Organization'),
                dict(id='description', name='Description'),
                ],
                data=[dict(organization='TBD', description='TBD')],
                ),
            style={'width': '50%','height':'50vh', 'display': 'inline-block','position': 'absolute'})],style={'width': '100%','height':'50vh'},id="fig2")

],id="div_global")


def create_pie_chart(name_orga):

    data_day = data["metadata-all"]["fr"]["day"]

    dict_pie_orga ={}

    data_year_sorted = sorted(data_day.keys(),key=int)
    for year in data_year_sorted:
        data_month_sorted = sorted(data_day[str(year)].keys(),key=int)
        for month in data_month_sorted:
            data_day_sorted = sorted(data_day[str(year)][str(month)].keys(),key=int)
            for day in data_day_sorted:
                if name_orga in list(data_day[str(year)][str(month)][str(day)]["org"].keys()):
                    for org in list(data_day[str(year)][str(month)][str(day)]["org"].keys()):
                        if str(org) != str(name_orga):
                            if org in dict_pie_orga:
                                dict_pie_orga[org] = dict_pie_orga[org] + data_day[str(year)][str(month)][str(day)]["org"][str(org)]
                            else:
                                dict_pie_orga[org] = data_day[str(year)][str(month)][str(day)]["org"][str(org)]

    dict_pie_orga_cut = dict(sorted(dict_pie_orga.items(), key=operator.itemgetter(1), reverse=True)[:10])
    
    df = pd.DataFrame.from_dict(dict_pie_orga_cut, orient= 'index',columns=['Number'])
    fig = px.pie(df,values=df['Number'],names=df.index.values,height = 667)
    fig.update_layout(title_text="Most mentioned Organizations with " + str(name_orga),title_x=0.5)

    return fig

@callback(
    Output("graph1", "figure"),
    Input("graph1","figure"))
def update_bar_chart(value):
    fig = create_org_bar_chart()
    return fig



@callback(
    Output("graph2", "figure"),
    Input("graph1","clickData"))
def update_pie_chart(clickData):

    if clickData != None:
        name_orga = clickData["points"][0]["id"]
        fig = create_pie_chart(name_orga)
    else:
        fig = px.scatter_3d().add_annotation(text="Please select an Organization", showarrow=False , font={"size":20})
    return fig


@callback(
    Output("table_org", "data"),
    Input("graph1","clickData"))
def update_table(clickData):

    if ctx.triggered_id == "graph1" : 

        if clickData != None:
            name_orga = str(clickData["points"][0]["id"])

            page_py = wiki_wiki.page(name_orga)
            if page_py.exists():
                descriptions = page_py.summary
                return [dict(organization=name_orga, description=descriptions)]
            else:
                descriptions = "Descriptions introuvable"
                return [dict(organization=name_orga, description=descriptions)]

    return [dict(organization='TBD', description='TBD')]