'''
Create master dataset for house price data at the county level
'''

import json
from urllib.request import urlopen
import pandas as pd

# Load county shapefiles
from urllib.request import urlopen
import json

# Load geojson
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


# Load datasets

# Zillow house prices
zhvi = pd.read_csv("zillow_home_value_index_county.csv", index_col="RegionID")

# Median income
med_inc = pd.read_csv("census_2020_median_inc_and_poverty.csv", dtype={'state': object, 'fips_county': object})

# Zillow RegionID to County FIPS code crosswalk
crosswalk = pd.read_csv("CountyCrossWalk_Zillow.csv", encoding = "ISO-8859-1", index_col="CountyRegionID_Zillow", dtype={"FIPS" : object})

# Population estimates
population = pd.read_csv("county_population.csv", encoding = "ISO-8859-1", dtype={"STATE" : object, "COUNTY" : object})

# Parks
natl_parks = pd.read_csv("natl_parks.csv")

population["STATE"] = population["STATE"].str.zfill(2)
population["COUNTY"] = population["COUNTY"].str.zfill(3)
population["COUNTY_FIPS"] = population["STATE"] + population["COUNTY"]

med_inc["state"] = med_inc['state'].str.zfill(2)
med_inc['County Code'] = med_inc["state"] + med_inc["fips_county"]

years = zhvi.loc[:, "2019-01-31":"2021-12-31":1]

regions = zhvi.loc[:, "SizeRank":"MunicipalCodeFIPS":1]

zhvi2 = regions.join(years)

zhvi2["2019_average"] = zhvi2.loc[:, "2019-01-31":"2019-12-31": 1].mean(axis=1)
zhvi2["2020_average"] = zhvi2.loc[:, "2020-01-31":"2020-12-31": 1].mean(axis=1)
zhvi2["2021_average"] = zhvi2.loc[:, "2021-01-31":"2021-12-31": 1].mean(axis=1)
zhvi2["2020_increase"] = ((zhvi2["2020_average"] - zhvi2["2019_average"])/zhvi2["2019_average"])*100
zhvi2["2021_increase"] = ((zhvi2["2021_average"] - zhvi2["2020_average"])/zhvi2["2020_average"])*100
zhvi2["2021_2yr_increase"] = ((zhvi2["2021_average"] - zhvi2["2019_average"])/zhvi2["2019_average"])*100

zhvi2["text_20"] = " "
zhvi2["text_21"] = " "
zhvi2["text_2yrs"] = " "

zhvi2.dropna()

zhvi_county = pd.merge(zhvi2, crosswalk, left_index=True, right_index=True)
zhvi_county["FIPS"] = zhvi_county["FIPS"].str.zfill(5)
zhvi_county_inc = pd.merge(zhvi_county, med_inc, left_on="FIPS", right_on="County Code")
zhvi_county_inc_pop = pd.merge(zhvi_county_inc, population, left_on="FIPS", right_on="COUNTY_FIPS")

# Format text for hovering
for idx, row in zhvi_county_inc_pop.iterrows():
    zhvi_county_inc_pop.at[idx, 'text_20'] = 'County:' + row["RegionName"] + '<br>' + 'State:' + row["State"] + \
    '<br>' + '2019-20 increase:' + str(round(row["2020_increase"], 3)) + '<br>' + 'Med_Inc:' + str(row["med_inc"]) + \
        '<br>' + 'Pop_2019:' + str(row["POPESTIMATE2019"])
    
    zhvi_county_inc_pop.at[idx, 'text_21'] = 'County:' + row["RegionName"] + '<br>' + 'State:' + row["State"] + \
    '<br>' + '2020-21 increase:' + str(round(row["2021_increase"], 3)) + '<br>' + 'Med_Inc:' + str(row["med_inc"]) + \
        '<br>' + 'Pop_2020:' + str(row["POPESTIMATE2020"])
    
    zhvi_county_inc_pop.at[idx, 'text_2yrs'] = 'County:' + row["RegionName"] + '<br>' + 'State:' + row["State"] + \
    '<br>' + '2019-21 increase:' + str(round(row["2021_2yr_increase"], 3)) + '<br>' + 'Med_Inc:' + str(row["med_inc"]) + \
        '<br>' + 'Pop_2020:' + str(row["POPESTIMATE2020"])

med_pov = zhvi_county_inc_pop['pov_rate'].median()
med_inc = zhvi_county_inc_pop['med_inc'].median()

zhvi_county_inc_pop['house_pov_ind'] = ((zhvi_county_inc_pop['pov_rate']>= med_pov) \
                                         | (zhvi_county_inc_pop['med_inc']<= med_inc)) \
                                         & (zhvi_county_inc_pop['2021_2yr_increase'] >= 30)
    
zhvi_county_inc_pop['opacity'] = zhvi_county_inc_pop['house_pov_ind'].apply(lambda x: 1 if x==True else 0.2)

#--------MOBILITY---------------#

def clean_mobility_data(): 
    """
    
    """
    mobi = pd.read_csv("google_mobility_county.csv", dtype= {"countyfips": str})
    mobi = mobi.replace(".", None)
    mobi[["gps_retail_and_recreation", "gps_grocery_and_pharmacy",
        "gps_parks", "gps_transit_stations", "gps_workplaces","gps_residential", "gps_away_from_home"]] = mobi[["gps_retail_and_recreation", "gps_grocery_and_pharmacy",
        "gps_parks", "gps_transit_stations", "gps_workplaces","gps_residential", "gps_away_from_home"]].apply(pd.to_numeric)

    mobi["countyfips"]= mobi["countyfips"].str.zfill(5)
    mobi["date"] = pd.to_datetime(mobi[["year", "month", "day"]])

    return mobi

mobility = clean_mobility_data()
