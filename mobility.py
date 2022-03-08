import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def clean_mobility_data(): 
    """
    
    
    """
    mobility = pd.read_csv("google_mobility_county.csv", dtype= {"countyfips": str})
    mobility = mobility.replace(".", None)
    mobility[["gps_retail_and_recreation", "gps_grocery_and_pharmacy",
        "gps_parks", "gps_transit_stations", "gps_workplaces","gps_residential", "gps_away_from_home"]] = mobility[["gps_retail_and_recreation", "gps_grocery_and_pharmacy",
        "gps_parks", "gps_transit_stations", "gps_workplaces","gps_residential", "gps_away_from_home"]].apply(pd.to_numeric)

    mobility["countyfips"]= mobility["countyfips"].str.zfill(5)
    mobility["date"] = pd.to_datetime(mobility[["year", "month", "day"]])

    return mobility

def create_mobility_graph(mobility, FIPS): 
    """
    Creates a time series graph for a specific FIPS code showing the
    various google mobility metrics for that county

    Inputs: 
        mobility (pandas dataframe) - mobility dataset
        FIPS (str) - county FIPS code

    Returns: 
        plotly graph
    """

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == FIPS]["date"],
        y= mobility[mobility["countyfips"] == FIPS]["gps_parks"],
        name = 'Mobility near parks', # Style name/legend entry with html tags
        connectgaps=True # override default to connect the gaps
    ))
    fig.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == FIPS]["date"],
        y= mobility[mobility["countyfips"] == FIPS]["gps_retail_and_recreation"],
        name = 'Mobility near retail and recreation', # Style name/legend entry with html tags
        connectgaps=True # override default to connect the gaps
    ))
    fig.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == FIPS]["date"],
        y= mobility[mobility["countyfips"] == FIPS]["gps_grocery_and_pharmacy"],
        name = 'Mobility -grocery and pharmacy', # Style name/legend entry with html tags
        connectgaps=True # override default to connect the gaps
    ))
    fig.add_trace(go.Scatter(
        x= mobility[mobility["countyfips"] == FIPS]["date"],
        y= mobility[mobility["countyfips"] == FIPS]["gps_residential"],
        name = 'Mobility -residential', # Style name/legend entry with html tags
        connectgaps=True # override default to connect the gaps
    ))

    fig.show()