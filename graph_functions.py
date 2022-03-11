import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

'''
Functions for app graphs
'''

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

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=FIPS)

    fig.update_layout(title="Percent change in GPS activity by Category")

    return fig

def create_income_graph(zhvi_county_inc_pop, FIPS):
    '''
    Create county income distribution graph
    '''

    fig = make_subplots(rows=2, cols=1)

    fig.add_trace (px.histogram(zhvi_county_inc_pop, x="med_inc"))
    fig.add_vline(x=np.median(zhvi_county_inc_pop.med_inc), line_dash = 'dash', line_color = 'green')
    fig.add_vline(x=float(zhvi_county_inc_pop.loc[zhvi_county_inc_pop["FIPS"] == FIPS, 'med_inc']), line_dash = 'dash', line_color = 'firebrick')
    fig.update_layout(title="Distribution of Median Incomes of Counties <br> Red line = selected county")

    fig.add_trace(px.histogram(zhvi_county_inc_pop, x="pov_rate"))
    fig.add_vline(x=np.median(zhvi_county_inc_pop.pov_rate), line_dash = 'dash', line_color = 'green')
    fig.add_vline(x=float(zhvi_county_inc_pop.loc[zhvi_county_inc_pop["FIPS"] == "30029", 'pov_rate']), line_dash = 'dash', line_color = 'firebrick')
    fig.update_layout(title="Distribution of Poverty rate of counties")


    return fig