from dash import dcc, html, Input, Output
from app import app
from apps import scatter_layout, histogram_layout, line_layout, treemap_layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Home | ', href='/'),
        dcc.Link('Scatter | ', href='/apps/scatter_layout'),
        dcc.Link('Histogram | ', href='/apps/histogram_layout'),
        dcc.Link('Treemap | ', href='/apps/treemap_layout'),
        dcc.Link('LineChart | ', href='/apps/line_layout')
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
    if pathname == '/apps/treemap_layout':
        return treemap_layout.layout
    if pathname == '/apps/line_layout':
        return line_layout.layout
    if pathname == '/':
        return "Please choose a link"

if __name__ == '__main__':
    app.run_server(debug=False)
    
#Exercise
# 1. Change menu3 to another graph (Not histogram)
# 2. Add the 4th menu (menu4) link to line graph
