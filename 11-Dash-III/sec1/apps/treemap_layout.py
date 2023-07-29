# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from app import app

df = pd.read_csv('https://github.com/chris1610/pbpython/blob/master/data/cereal_data.csv?raw=True')

fig2 = px.treemap(
                 df, 
                 path=['shelf', 'mfr'], 
                 values='cereal', 
                 title='Cereals by shelf location'
                )

layout = html.Div(children=[

      html.H1(children='Treemap'),

        html.Div(children='''
            My description treemap.
        '''),

        dcc.Graph(
            id='tm1',
            figure=fig2
        )
    
     ], style={'padding': 10, 'flex': 1})
'''
@app.callback(
    Output('example-graph3', 'figure'),
    Input('nbin-slider2', 'value'))
def update_figure(x):

    fig2 = px.histogram(df, x='sugars', title='Rating distribution',nbins=x)
    
    #fig2.update_layout(transition_duration=500)
    
    return fig2
'''