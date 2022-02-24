
import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

counties["features"][0]

df = pd.read_csv("google_mobility_county.csv")

recent_data = df[(df["year"] == 2022) & (df["month"] == 2) & (df["day"]== 12)]
recent_data = recent_data.rename(columns={"countyfips": "fips"})

fig = px.choropleth(recent_data, geojson=counties, locations='fips', color='gps_parks',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'gps_parks':'change in mobility near parks'}
                          )
