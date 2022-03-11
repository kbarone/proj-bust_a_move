from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import json
from urllib.request import urlopen
import plotly.graph_objects as go
from dash.dependencies import Input, Output



app = Dash(__name__)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

exec(open("zhvi_cleaning.py").read())

# Figure 1
fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=zhvi_county_inc_pop["FIPS"], z=zhvi_county_inc_pop["2021_2yr_increase"],
                                    colorscale="Jet", zmin=-17, zmax=58, text=zhvi_county_inc_pop["text_2yrs"], 
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(clickmode='event+select')



app.layout = html.Div([

    html.Div([
        dcc.Graph(
            id='zhvf',
            clickData={'points': [{'location': 'Japan'}]},
            figure=fig
    )], style={'width': '60%','display': 'inline-block'}),

    html.Div([
        dcc.Graph(
            id='mobility',
    )],style={'width': '40%', 'display': 'inline-block'}),

    html.Div([
            dcc.Markdown(),
            html.Pre(id='click-data', style=styles['pre'])
    ], className='three columns'),
])

@app.callback(
    Output('click-data', 'children'),
    [Input('zhvf', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData['points'][0]['location'], indent=2)


@app.callback(
    Output('mobility', 'figure'),
    [Input('zhvf', 'clickData')])
def update_time_series(clickData):
    # Figure 2
    county = clickData['points'][0]['location']
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == county]["date"],
        y= mobility[mobility["countyfips"] == county]["gps_parks"],
        name = 'parks', 
        connectgaps=True
    ))
    fig2.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == county]["date"],
        y= mobility[mobility["countyfips"] == county]["gps_retail_and_recreation"],
        name = 'retail and recreation', 
        connectgaps=True
    ))
    fig2.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == county]["date"],
        y= mobility[mobility["countyfips"] == county]["gps_grocery_and_pharmacy"],
        name = 'grocery and pharmacy',
        connectgaps=True
    ))
    fig2.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == county]["date"],
        y= mobility[mobility["countyfips"] == county]["gps_residential"],
        name = 'residential', 
        connectgaps=True
    ))
    fig2.update_layout(legend=dict(
        yanchor="top",
        y=1.5,
        xanchor="left",
        x=0.01
    ))
    fig2.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=county)

    return fig2




if __name__ == '__main__':
    app.run_server(debug=True)

