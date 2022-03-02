
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



zhvf = pd.read_csv("zillow_home_value_forecast.csv", dtype = {"RegionName" : str})
zhvf_zip = zhvf[zhvf["Region"] == "Zip"]

zip_county = pd.read_csv("ZIP_COUNTY_122021.csv", dtype = {"zip": str, "county": str})
zc = zip_county[["zip", "county"]]
zc = zc.astype({"zip" : str})
zhvf_zip = zhvf_zip.astype({"RegionName" : str})

zhvf_zip_county = pd.merge(zhvf_zip, zc, left_on='RegionName', right_on='zip')
zhvf_zip_county

census = pd.read_csv("census_2020_median_inc.csv")



fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=zhvf_zip_county.county, z=zhvf_zip_county.ForecastYoYPctChange,
                                    colorscale="Viridis", zmin=0, zmax=50,
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()