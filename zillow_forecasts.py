import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def county_data():
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    return counties

def clean_zhvf_data():
    
    zhvf = pd.read_csv("zillow_home_value_forecast.csv", dtype = {"RegionName" : str})
    zhvf_zip = zhvf[zhvf["Region"] == "Zip"]
    zip_county = pd.read_csv("ZIP_COUNTY_122021.csv", dtype = {"zip": str, "county": str})
    zc = zip_county[["zip", "county"]]
    zc = zc.astype({"zip" : str})
    zhvf_zip = zhvf_zip.astype({"RegionName" : str})
    zhvf_zip_county = pd.merge(zhvf_zip, zc, left_on='RegionName', right_on='zip')
    zhvf_zip_county
    zhvf_agg_county = zhvf_zip_county.groupby('county')['ForecastYoYPctChange'].mean().reset_index()
    zhvf_agg_county.columns = ["county", "mean_forecast_pct_change"]
    zhvf_agg_county
    
    return zhvf_agg_county

#mean_forecast_pct_change
#zhvf_agg_county
def create_zillow_map(data, level, metric):
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    fig = go.Figure(go.Choroplethmapbox(geojson = counties, locations = data[level], z = data[metric],
                                        colorscale="Jet", zmin=0, zmax=40,
                                        marker_opacity=0.5, marker_line_width=0))
    fig.update_layout(mapbox_style="carto-positron",
                    mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

#rental data is not interesting
def clean_zillow_rental():
    rental_raw = pd.read_csv("zillow_rentals.csv", dtype= {"RegionName": str})
    zip_county = pd.read_csv("ZIP_COUNTY_122021.csv", dtype = {"zip": str, "county": str})
    zc = zip_county[["zip", "county"]]
    zc = zc.astype({"zip" : str})
    rentals = pd.merge(rental_raw, zc, left_on='RegionName', right_on='zip')
    rental_time_series = rentals[:][:]
    rentals["2019_average"] = rentals.loc[:, "2019-01":"2019-12": 1].mean(axis=1)
    rentals["2020_average"] = rentals.loc[:, "2020-01":"2020-12": 1].mean(axis=1)
    rentals["2021_average"] = rentals.loc[:, "2021-01":"2021-12": 1].mean(axis=1)
    rentals["2020_increase"] = ((rentals["2020_average"] - rentals["2019_average"])/rentals["2019_average"])*100
    rentals["2021_increase"] = ((rentals["2021_average"] - rentals["2020_average"])/rentals["2020_average"])*100
    rentals["2019_to_2021"] = ((rentals["2021_average"] - rentals["2019_average"])/rentals["2021_average"])*100

    rental_time_series = rental_time_series.melt(id_vars = ["RegionID", "RegionName", "SizeRank", "MsaName","zip", "county"])
    rental_time_series = rental_time_series.rename(columns = {"variable": "Date"})

    rentals_agg = rentals.groupby('county')['2019_to_2021'].mean().reset_index()
    rentals_agg.columns = ["county", "2019_to_2021"]

    return rentals_agg, rental_time_series
