import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

'''
Functions for all of the apps Graphs
'''

def create_chloropleth(counties, zhvi_county_inc_pop, natl_parks):
    '''
    Main chloropleth map

    Inputs:
    counties : (pandas dataframe) geojson shapefiles of US counties
    zhvi_county_inc_pop : (pandas dataframe) county-level dataset of house prices, med income, poverty rate
    natl_parks : (pandas dataframe) lat-long of national parks in the US

    Returns:
    plotly chloropleth map

    '''
    fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=zhvi_county_inc_pop["FIPS"], \
                                    z=zhvi_county_inc_pop["2021_2yr_increase"],
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

    return fig




def create_mobility_graph(mobility, zhvi_county_inc_pop, FIPS): 
    """
    Creates a time series graph for a specific FIPS code showing the
    various google mobility metrics for that county

    Inputs: 
        mobility (pandas dataframe) - mobility dataset
        FIPS (str) - county FIPS code

    Returns: 
        plotly graph object
    """

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == FIPS]["date"],
        y= mobility[mobility["countyfips"] == FIPS]["gps_parks"],
        name = 'Mobility near parks',
        connectgaps = True
    ))
    fig.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == FIPS]["date"],
        y= mobility[mobility["countyfips"] == FIPS]["gps_retail_and_recreation"],
        name = 'Mobility near retail and recreation',
        connectgaps = True
    ))
    fig.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == FIPS]["date"],
        y= mobility[mobility["countyfips"] == FIPS]["gps_grocery_and_pharmacy"],
        name = 'Mobility -grocery and pharmacy',
        connectgaps = True
    ))
    fig.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == FIPS]["date"],
        y= mobility[mobility["countyfips"] == FIPS]["gps_residential"],
        name = 'Mobility -residential',
        connectgaps = True
    ))

    fig.add_annotation(x=0, y=1.10, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=str(FIPS +\
                           zhvi_county_inc_pop.loc[zhvi_county_inc_pop["FIPS"] == \
                               FIPS,'RegionName'].to_string().split(" ", 1)[-1]))

    fig.update_layout(legend=dict(
        yanchor="bottom",
        y= -0.75,
        xanchor="left",
        x=0.01
    ))

    return fig

def create_mobility_graph2(mobility, zhvi_county_inc_pop, FIPS):
    df = mobility[mobility["countyfips"] == FIPS]
    df = df.rename({"gps_parks" : "Parks", "gps_retail_and_recreation": "Retail and Recreation", "gps_grocery_and_pharmacy" : "Grocery and Pharmacy"}, axis=1)
    fig = px.scatter(df, x="date", y=["Parks", "Retail and Recreation", "Grocery and Pharmacy"], trendline="expanding", labels = {"variable": "Type of Activity"})

    fig.update_traces(showlegend=True) 
    fig.update_traces(visible=False, selector=dict(mode="markers"))
    fig.update_layout(legend=dict(
        yanchor="bottom",
        y= -0.75,
        xanchor="left",
        x=0.01
    ))
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=str(FIPS +\
                           zhvi_county_inc_pop.loc[zhvi_county_inc_pop["FIPS"] == \
                               FIPS,'RegionName'].to_string().split(" ", 1)[-1]))

    fig.update_layout(title="Percent change in GPS activity by Category")

    return fig


def create_income_graph(zhvi_county_inc_pop, FIPS):
    '''
    Creates histogram of county median income distribution and
    histogram of poverty rates across counties

    Inputs-
    zhvi_county_inc_pop : (pandas dataframe) county level median income and poverty data
    FIPS : (str) county FIPS code

    Returns-
    plotly graph object
    '''

    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(go.Histogram(x=zhvi_county_inc_pop["med_inc"], name="Median income"), 1, 1)
    fig.add_shape(
        go.layout.Shape(type='line', xref='x',
                        x0=np.median(zhvi_county_inc_pop.med_inc), y0=0.0, 
                        x1=np.median(zhvi_county_inc_pop.med_inc),
                        y1=200,
                        line={'dash': 'dash', 'color':'blue'}), row=1, col=1)
    fig.add_shape(
        go.layout.Shape(type='line', xref='x',
                        x0=float(zhvi_county_inc_pop.loc[zhvi_county_inc_pop["FIPS"] == FIPS, 'med_inc']),
                        y0=0.0, 
                        x1=float(zhvi_county_inc_pop.loc[zhvi_county_inc_pop["FIPS"] == FIPS, 'med_inc']),
                        y1=200,
                        line={'dash': 'solid', 'color':'black'}), row=1, col=1)

    # pov_rate
    fig.add_trace(go.Histogram(x=zhvi_county_inc_pop["pov_rate"], name="Poverty rate"), 2, 1)
    fig.add_shape(
        go.layout.Shape(type='line', xref='x',
                        x0=np.median(zhvi_county_inc_pop.pov_rate), 
                        y0=0.0,
                        x1=np.median(zhvi_county_inc_pop.pov_rate),
                        y1=140,
                        line={'dash': 'dash', 'color':'blue'}), row=2, col=1)
    fig.add_shape(
        go.layout.Shape(type='line', xref='x',
                        x0=float(zhvi_county_inc_pop.loc[zhvi_county_inc_pop["FIPS"] == FIPS, 'pov_rate']), y0=0.0, 
                        x1=float(zhvi_county_inc_pop.loc[zhvi_county_inc_pop["FIPS"] == FIPS, 'pov_rate']),
                        y1=140,
                        line={'dash': 'solid', 'color':'black'}), row=2, col=1)
    
    fig.add_annotation(x=0, y=1.0, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=str('black line: ' + FIPS+\
                           zhvi_county_inc_pop.loc[zhvi_county_inc_pop["FIPS"] == \
                               FIPS,'RegionName'].to_string().split(" ", 1)[-1]+\
                               "<br>" + 'blue line: median value'))
    return fig

def create_pie_chart(zhvi_county_inc_pop, FIPS, race):
    '''
    Create pie chart of race distribution for a county

    Inputs-
    zhvi_county_inc_pop : (pandas dataframe) county level median income and poverty data
    FIPS : (str) county FIPS code
    race : (pandas dataframe) county level data on race distribution

    Returns-
    plotly graph object
    '''

    if len(race.loc[race["fips"] == FIPS]) == 0:
        fig = px.pie(title='No race data for this selection')
    
    else:
        fig = px.pie(race, values=race[race['fips']==FIPS]['perc_total'], names=race['race'].unique(),
             title=str('Racial breakdown' + "-" + zhvi_county_inc_pop.loc[zhvi_county_inc_pop["FIPS"] == \
                               FIPS,'RegionName'].to_string().split(" ", 1)[-1])
                )
        fig.update_traces(textposition='inside', textinfo='percent')

    return fig