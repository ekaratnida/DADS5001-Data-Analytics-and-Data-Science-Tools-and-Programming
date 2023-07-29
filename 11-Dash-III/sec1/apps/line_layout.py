# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from app import app

df = pd.read_csv('https://github.com/chris1610/pbpython/blob/master/data/cereal_data.csv?raw=True')

lineFig = px.line(df, x='sugars',y='rating', color='mfr', title='Rating distribution')

layout = html.Div(children=[

      html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='lineID',
            figure=lineFig
        ),

       ''' dcc.Slider(
            1,
            10,
            step=None,
            value=3,
            marks={str(i): str(i) for i in range(11)},
        id='nbin-slider2'
        ) '''
    
     ], style={'padding': 10, 'flex': 1})
'''
@app.callback(
    Output('lineID', 'figure'),
    Input('nbin-slider2', 'value'))
def update_figure(x):

    fig2 = px.histogram(df, x='sugars', title='Rating distribution',nbins=x)
    
    #fig2.update_layout(transition_duration=500)
    
    return fig2
''' 