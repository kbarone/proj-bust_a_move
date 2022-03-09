from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import json
from urllib.request import urlopen
import plotly.graph_objects as go


app = Dash(__name__)


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

counties["features"][0]

zhvf = pd.read_csv("zillow_home_value_forecast.csv", dtype = {"RegionName" : str})
zhvf_zip = zhvf[zhvf["Region"] == "Zip"]

zip_county = pd.read_csv("ZIP_COUNTY_122021.csv", dtype = {"zip": str, "county": str})
zc = zip_county[["zip", "county"]]
zc = zc.astype({"zip" : str})
zhvf_zip = zhvf_zip.astype({"RegionName" : str})
zhvf_zip_county = pd.merge(zhvf_zip, zc, left_on='RegionName', right_on='zip')

max_forecast = zhvf_zip_county["ForecastYoYPctChange"].max()
min_forecast = zhvf_zip_county["ForecastYoYPctChange"].min()

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=zhvi_county_inc_pop["FIPS"], z=zhvi_county_inc_pop["2021_2yr_increase"],
                                    colorscale="Jet", zmin=-17, zmax=58, text=zhvi_county_inc_pop["text_2yrs"], 
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


app.layout = html.Div([
    dcc.Graph(
        id='zhvf',
        figure=fig
    ),

])

if __name__ == '__main__':
    app.run_server(debug=True)

