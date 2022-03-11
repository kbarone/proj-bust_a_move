from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import json
from urllib.request import urlopen
import plotly.graph_objects as go
from dash.dependencies import Input, Output



app = Dash(__name__)

colors = {
    'background': '#FDFEFE',
    'text': '#17202A'
}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

exec(open("zhvi_cleaning.py").read())
natl_parks = pd.read_csv("natl_parks.csv")

# Figure 1
fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=zhvi_county_inc_pop["FIPS"], z=zhvi_county_inc_pop["2021_2yr_increase"],
                                    colorscale="Jet", zmin=-17, zmax=58, text=zhvi_county_inc_pop["text_2yrs"], 
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron", # style options: "basic", "streets", "outdoors", 
                # "dark", "satellite", or "satellite-streets","light"
                # "open-street-map", "carto-positron", 
                # "carto-darkmatter", "stamen-terrain", 
                # "stamen-toner" or "stamen-watercolor"
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(
    title="Changes in Housing Prices from 2019 to 2021")
fig.add_trace(go.Scattermapbox(
    lat= natl_parks['latitude'],
    lon= natl_parks['longitude'],
    mode ='markers',
    marker=go.scattermapbox.Marker(
        size=6,
        color = 'black'),
    text = natl_parks["park_name"], hoverinfo = 'skip'))
fig.update_layout(title={
        'text': "Percent Change in Housing Prices from 2019 to 2021",
        'y': 0.96,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.update_layout(clickmode='event+select')




app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1(
        children='Bust A Move!',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Exploring Regional Mobility in the US\n', style={
        'textAlign': 'center',
        'color': colors['text']
    }),


    html.Div(children='Click on a county on the map to view mobility and demographic data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([
        dcc.Graph(
            id='zhvf',
            clickData={'points': [{'location': '30029'}]},
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
        name = 'Parks', 
        connectgaps=True
    ))
    fig2.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == county]["date"],
        y= mobility[mobility["countyfips"] == county]["gps_retail_and_recreation"],
        name = 'Retail and Recreation', 
        connectgaps=True
    ))
    fig2.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == county]["date"],
        y= mobility[mobility["countyfips"] == county]["gps_grocery_and_pharmacy"],
        name = 'Grocery and Pharmacy',
        connectgaps=True
    ))
    fig2.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == county]["date"],
        y= mobility[mobility["countyfips"] == county]["gps_residential"],
        name = 'Residential', 
        connectgaps=True
    ))
    fig2.update_layout(legend=dict(
        yanchor="bottom",
        y= -0.75,
        xanchor="left",
        x=0.01
    ))
    fig2.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=county)

    fig2.update_layout(title="Percent change in GPS activity by Category")

    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)

