# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import flask
import plotly.plotly as py
from plotly import graph_objs as go
import math
from lifetimes import BetaGeoFitter

df = pd.read_csv(
    'https://gist.githubusercontent.com/lksfr/c65d53e66ef45673ce4c8f5ef23e2645/raw/c3dc295facb571959dccc917797158b81d032ac2/CLV.csv',
    index_col=False)
df2 = pd.read_csv('https://gist.githubusercontent.com/lksfr/ae394805cb25c961e5284fd9215997a8/raw/a4ded8cda256058a7ee2de588eedef923a0e4066/df2.csv')
df2.drop('Unnamed: 0', axis=1, inplace=True)

df = df.drop("Unnamed: 0", axis=1)

summary2 = pd.read_csv('https://gist.githubusercontent.com/lksfr/cc8488828a89419a50c0486f94f6092a/raw/9c8dfbd080d3a5eaf2b02eab4053c3915156e965/summary2.csv'
    ,index_col='Shipping Company')

bgf = BetaGeoFitter()
bgf.load_model('bgf.pkl')

app = dash.Dash()

app.layout = html.Div([
        # header
        html.Div([
            html.Div(
                html.Img(src='https://i.ibb.co/G74pSt4/transparant.png',height="100%")
                ,style={"float":"left","height":"100%", "margin-top": "0px"})
            ],
            className="row header",style={"background-color": "#ffffff"}
            ),

        # tabs
        html.Div([
           # html.Div([
            dcc.Tabs(id="tabs", value='tab-1',children=[
                
                dcc.Tab(label='Customer Lifetime Value', 
                        value='tab-1',
                        children=[
                        #styling
                        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet"),


                        html.Div([
                            html.H3("Customer Repeat Purchases"),

                            dcc.Dropdown(
                                id='customer_prob',
                                options=[
                                {'label': i, 'value': i} for i in df.ID.unique()
                             ],
                            placeholder='Select customer...'
                         ),

                      #   html.P(style={"margin-top": "17px"}),
                      #  html.P(),

                        
                        dcc.Slider(
                            id='slider',
                            min=0,
                            max=12,
                            marks={i: 'Month {}'.format(i) if i == 1 else str(i) for i in range(1, 13)},
                            value=5,

                    )
                        ,
                html.Br(),
                html.Br(),

                html.Div(id='result', style={"width": "95%"})


                ]

                ,style={"float":"right", "margin-top": "20px", "background-color": "white", "margin-right": "5%", "height": "260px", "width": "40%", "padding-right": "20px", "padding-left": "20px", "border-radius": "25px",
                "border": "2px solid #4286f4" }
                ),




                    html.Div([

                        html.H3("Customer Lifetime Value", style={"padding-left": "150px", "padding-right": "17px"}),

                        html.Div([
                        dcc.Dropdown(id='dropdown', style={'width': '60%', "padding-left": "150px"}, options=[
                            {'label': i, 'value': i} for i in df.ID.unique()
                            ], multi=True, placeholder='Filter by customer name...')
                        ], style={'width': '600px'}),
                        html.Br(),

                        html.Div([
                        dcc.Dropdown(id='dropdown2', style={'width': '60%', "padding-left": "150px"}, options=[
                            {'label': i, 'value': i} for i in df.Target_Group.unique()
                            ], multi=True, placeholder='Filter by target group...')

                        ], style={'width': '600px'}),
                        html.Div([

                            dt.DataTable(
                            # Initialise the rows
                            rows=df.to_dict("records"),
                            row_selectable=True,
                            filterable=True,
                            sortable=True,
                            selected_row_indices=[],
                            id='table'
                        )                            
                        ], style = {'width':'95%', 'margin-top': '15px', 'margin-left': '15px', 'margin-bottom': '20px'})
                        ],style={"float":"left", "background-color": "white", "background-color": "white", "margin-left": "5%", "padding-left": "-10px" , "width": "40%", "left": "-10px", "border-radius": "25px",
                        "border": "2px solid #4286f4", "margin-top": "20px"}
                    )

             #   ])
                ]),

                dcc.Tab(label='Recommendation', 
                       # style={"height":"20","verticalAlign":"middle", "text-align": "center"},
                        children=[
                    html.Div([
                        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet"),

                        html.H3("Some CLV Analysis")
                    ])
                ]),

                dcc.Tab(label='About This Project', 
                       # style={"height":"20","verticalAlign":"middle", "text-align": "center"},
                        children=[
                    html.Div([
                        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet"),

                        html.Div([
                        html.H3("About This Project"),

                        html.P("This dashboard is the final product of the Capstone Project of Raymond Liang, Lukas Frei, Jialan Zhu, Esther Chang, Bird, and Iris (Jo Wen) Chen."),
                        html.P("We designed the dashboard with the intention of making it easily usable and understandable."),
                        html.P( "Add more text..."),
                        html.P("Link to our GitHub repository:"), html.A("https://github.com/estherc1/NOSO")

                        ], style={"background-color": "white", "background-color": "white", "margin-left": "5%", "margin-right": "5px", "padding-left": "10px" ,"padding-bottom": "10px", "width": "80%",  "border-radius": "25px",
                        "border": "2px solid #4286f4", "margin-top": "20px"}
                        )
                    ])
                ])
            ])
        ])
    ])
                 

@app.callback(
    dash.dependencies.Output('table', 'rows'),
    [Input('dropdown', 'value'), Input('dropdown2', 'value')])

def update_table(dropdown, dropdown2):
    if dropdown is None and dropdown2 is None:
        return df.to_dict("records")

    else:
        dff = df[(df["Target_Group"].str.contains('|'.join(dropdown2))) & (df["ID"].str.contains('|'.join(dropdown)))]
        return dff.to_dict("records")
@app.callback(
    Output('result', 'children'),
    [Input('customer_prob', 'value'), Input('slider', 'value')])
def customer_order_prob(name, periods=1):
    if name is not None:
        try:
            t = periods
            individual = summary2.loc[name]
            individual_id = summary2.loc[name].index
            probability = bgf.predict(t, individual['frequency'], individual['recency'], individual['T'])
            return('This customer will make {:.2f} repeat purchases over the course of '.format(probability) + str(periods) + ' months.')
        except ValueError:
            return 'Invalid Input'

if __name__ == "__main__":
    app.run_server(debug=True)