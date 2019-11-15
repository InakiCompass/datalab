import dash
import dash_table
import pandas as pd
import flask
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output

url = 'https://raw.githubusercontent.com/InakiCompass/datalab/master/SG6'

df = pd.read_csv(url,sep=",")
#df = pd.read_csv(url,sep=",",header=[0,1],index_col=[0])#,index_col=0)
df1 = pd.read_csv(url,sep=",")
dg = df1.drop(df.index[0])

df.rename(columns={'Unnamed: 3_level_1':'','Unnamed: 4_level_1':' ','Issuer_Country':'  '},inplace=True)
df=round(df,1)
cols=([{'name':list(c),'id':c[1]} for c in df.columns.values])
#cols[1].update( {'hideable' : True})
df.columns=df.columns.droplevel(0)

navbar = dbc.NavbarSimple(
    
    brand="Compass Data lab",
    brand_href="#",
    color="primary",
    sticky="center",
)

theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

available_indicators = df1['Sector'].unique().tolist()
available_indicators.append("All")
# available_indicators_name = df1['Name'].unique().tolist()
# available_indicators_name.append("All")

body = html.Div(
    [
        #Dropdowns
        dbc.Row(
            [
                dbc.Col(html.Div(" "), width=1),
                dcc.Dropdown(
                    id='drop',
                    options=[{'label': i, 'value': i} for i in available_indicators[1:]],
                    value='All',
                    style={'width': '200px'}
                    ),
                # dcc.Dropdown(
                #     id='drop_name',
                #     options=[{'label': i, 'value': i} for i in available_indicators_name[1:]],
                #     value='All',
                #     style={'width': '200px'}
                #     )
            ]),
        
        #Graficos
        dbc.Row(
            [
                dbc.Col(html.Div(" "), width=1),
                dbc.Col(dcc.Graph(id='PE/ROE')),
                dbc.Col(dcc.Graph(id='ROIC/EVEBITDA')),
                dbc.Col(html.Div(" "), width=1),
                dbc.Col(html.Div(" "), width=1),
                ]),
        
        #Tabla
        dbc.Row([
            dbc.Col(html.Div(" "), width=1),
            dash_table.DataTable(
                
                id='datatable-filtering-fe',
                columns=cols,
                fixed_rows={'headers': True, 'data': 0},
                data=df.to_dict('records'),
                filter_action="native",
                merge_duplicate_headers=True,
                style_cell={'textAlign': 'center','fontSize':12, 'font-family':'sans-serif','padding': '1px', 'width': '40px'},
                style_data_conditional=[
                    { 'if': {'column_id':''},
                        'backgroundColor': 'GhostWhite'}, 
                    { 'if': {'column_id':'  '},
                        'backgroundColor': 'GhostWhite'},           
                    {'if': {'column_id':' '},
                        'backgroundColor': 'GhostWhite',
                        'border-right': '1px solid black'},
                    {'if': {'column_id':'Recom'},
                        'border-right': '1px solid grey'},
                    {'if': {'column_id':'2020'},
                        'border-right': '1px solid grey'},
                    {'if': {'column_id':'2020 '},
                        'border-right': '1px solid grey'},
                    {'if': {'column_id':'2020  '},
                        'border-right': '1px solid grey'},
                    {'if': {'column_id':'2020   '},
                        'border-right': '1px solid black'},
                    {'if': {'filter_query': '{s} eq 1'}, #'column_id': ' ',
                        'border-bottom': '1px solid grey'},
                    # {'if': {'row_index': 'odd'},
                    #   'backgroundColor': 'rgb(248, 248, 248)'},  
                    ],
                style_header={'backgroundColor': 'GhostWhite',
                    'fontWeight': 'bold',
                    'border': '1px solid black'},
                style_table={'width': '1600px', 'maxHeight': '1000px', 'overflowY': 'scroll', 'overflowX': 'scroll','align':'center', 'padding': 40},),
            html.Div(id='datatable-filter-container'),
            
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([navbar, body])


########### FUNCIONES #############

############# TABLA ############

# @app.callback(
#     Output('table', 'data'),
#     [Input('drop', 'value'),]
    
# )
# def update_datatable(drop):
    
#     #df = pd.read_csv('/home/inaki/Desktop/Compass_Data_Lab/SG6',header=[0,1],index_col=[0])#,index_col=0)

#     if drop == "All":
#         dk = df1[df1['Country'] == 'Colombia']
    
#     else:
#         dk = [df1['Country'] == drop]

#     #data = [{'name': i['name'], 'id': i['id']} for i in dk.to_dict('records')]
#     return df.to_dict('records')
#     #return df.to_dict('records')


############ GRAFICOS ###########

@app.callback(
    Output('PE/ROE', 'figure'),
    [Input('drop', 'value'),
    
])
def update_graph1(drop):
    
    if drop == "All":
        dgr = df1.drop(df.index[0])
    
    else:
        dgr = df1[df1['Sector'] == drop]

    return {
        'data': [
                go.Scatter(
                    x=dgr[dgr['Country'] == i]['P/E.2'],
                    y=dgr[dgr['Country'] == i]['ROE.2'],
                    text=dgr[dgr['Country'] == i]['Name'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in dgr.Country.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'P/E'},
                yaxis={'title': 'ROE'},
                margin={'l': 40, 'b': 50, 't': 50, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )}

@app.callback(
    Output('ROIC/EVEBITDA', 'figure'),
    [Input('drop', 'value'),
    
])
def update_graph2(drop):
    
    if drop == "All":
        dgr = df1.drop(df.index[0])
    
    else:
        dgr = df1[df1['Sector'] == drop]

    return {
        'data': [
                go.Scatter(
                    x=dgr[dgr['Country'] == i]['EV/EBITDA.2'],
                    y=dgr[dgr['Country'] == i]['ROIC.2'],
                    text=dgr[dgr['Country'] == i]['Name'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in dgr.Country.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'EV/EBITDA'},
                yaxis={'title': 'ROIC'},
                margin={'l': 40, 'b': 50, 't': 50, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )}

#################################


if __name__ == "__main__":
    app.run_server(debug=True)
