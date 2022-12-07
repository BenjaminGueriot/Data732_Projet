import dash
from dash import Dash, dcc, html, Input, Output, dash_table, callback, ctx
import dash_bootstrap_components as dbc
import os

CSS = [dbc.themes.SLATE]

all_data = [file_name for file_name in os.listdir() if '.json' in file_name]

def writefichier(nom_fichier):
    text_file = open("./data.txt", "w")
    text_file.write(nom_fichier)
    text_file.close()
    return

writefichier(all_data[len(all_data)-1])

app = Dash(__name__, use_pages=True, external_stylesheets=CSS)

def createlayout():

    app_layout = html.Div([html.H1('Visualisation Project by Thomas and Benjamin'), 
                        html.Div([
                            html.Div([
                                    html.Div(
                                        html.Ul( 
                                            html.H2(
                                                html.Li(
                                                    dcc.Link(
                                                        f"{page['name']}", href=page["relative_path"]
                                                    ))
                                        )),
                                    )
                                    for page in dash.page_registry.values()
                                ],style={'width': '50%', 'display': 'inline-block'}),
                            
                            html.Div([
                                    html.H2('Select a file :'),
                                    dcc.Dropdown(
                                            id="dropdown_global",
                                            options= all_data,
                                            value= all_data[len(all_data)-1],
                                            clearable=False,
                                            style={'width': '100%', 'top': '0px'}
                                    ),
                                ],style={'width': '50%','height' : "100%", 'display': 'inline-block', 'position': 'absolute'}),
                        ]),
                        html.Div(children=[html.Div(dash.page_container)],id="pages_container"),dcc.Location(id="url",refresh=True),
                        
                    ],id = "div_global")
    return app_layout

app.layout = createlayout()


@callback(
    Output("pages_container","children"),
    Input("dropdown_global", "value"))
def refresh(value):

    if ctx.triggered_id == "dropdown_global" :
        writefichier(value)
        return dash.page_container
    else:
        return dash.page_container

if __name__ == '__main__':
	app.run_server(debug=True)