from dash import dcc, html, Input, Output
from app import app
from apps import scatter_layout, histogram_layout, histogram_layout2

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Home | ', href='/'),
        dcc.Link('Scatter | ', href='/apps/scatter_layout'),
        dcc.Link('Histogram | ', href='/apps/histogram_layout'),
        dcc.Link('Menu3 | ', href='/apps/histogram_layout2')
    ], className="row"),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/scatter_layout':
        return scatter_layout.layout
    if pathname == '/apps/histogram_layout':
        return histogram_layout.layout
    if pathname == '/apps/histogram_layout2':
        return histogram_layout2.layout
    if pathname == '/':
        return "Please choose a link"

if __name__ == '__main__':
    app.run_server(debug=False)
    
#Exercise
# 1. Change menu 3 to another graph (Not histogram)
# 2. Add the 4th menu link to line graph
