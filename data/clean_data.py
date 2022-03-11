import pandas as pd
import numpy as np
import json
from urllib.request import urlopen

# Load county shapefiles
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
# Load datasets

# Zillow house prices
zhvi = pd.read_csv("zillow_home_value_index_county.csv", index_col="RegionID")

# Median income
med_inc = pd.read_csv("census_2020_median_inc.csv", dtype={'state': object, 'fips_county': object})

# Zillow RegionID to County FIPS code crosswalk
crosswalk = pd.read_csv("CountyCrossWalk_Zillow.csv", encoding = "ISO-8859-1", index_col="CountyRegionID_Zillow", dtype={"FIPS" : object})

# Population estimates
population = pd.read_csv("county_population.csv", encoding = "ISO-8859-1", dtype={"STATE" : object, "COUNTY" : object})


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

#--------MOBILITY---------------#

mobility = pd.read_csv("google_mobility_county.csv", dtype= {"countyfips": str})
mobility = mobility.replace(".", None)
#mobility = mobility.replace(0, None)
mobility[["gps_retail_and_recreation", "gps_grocery_and_pharmacy",
     "gps_parks", "gps_transit_stations", "gps_workplaces","gps_residential", "gps_away_from_home"]] \
         = mobility[["gps_retail_and_recreation", "gps_grocery_and_pharmacy", "gps_parks", \
             "gps_transit_stations", "gps_workplaces","gps_residential", "gps_away_from_home"]].apply(pd.to_numeric)

mobility["countyfips"]= mobility["countyfips"].str.zfill(5)
mobility["date"] = pd.to_datetime(mobility[["year", "month", "day"]])


df.to_csv("google_mobility_clean.csv")





# CLEAN RACE/ETHNICITY DATA

df = pd.read_csv("/Users/katybarone/Documents/uchicago/race_by_county.csv")

cols = {'NAME':	'County',
'B02001_001E': 'total',
'B02001_001M':	'moe_total',
'B02001_002E': 'white',
'B02001_002M':	'moe_white',
'B02001_003E':	'blk_af_am',
'B02001_003M':	'moe_blk_af_am',
'B02001_004E':	"am_indian_alas_nat",
'B02001_004M':	"moe_am_indian_alas_nat",
'B02001_005E':	"asian",
'B02001_005M':	"moe_asian",
'B02001_006E':	"nat_haw_pac_island",
'B02001_006M':	"moe_nat_haw_pac_island",
'B02001_007E':	"other",
'B02001_007M':	"moe_other",
'B02001_008E':	"two_or_more",
'B02001_008M':	"moe_two_or_more",
'B02001_009E':	"two_more_inc_other",
'B02001_009M':	"moew_two_more_inc_other",
'B02001_010E':	"two_more_excl_other_three",
'B02001_010M':	"moe_two_more_excl_other_three"}

df = df.rename(columns = cols)
df = df.iloc[1:]

cols_to_check = df.columns[:-3]
df['is_na'] = df[cols_to_check].isnull().apply(lambda x: all(x), axis=1) 
df = df[df['is_na']==False]
df = df.loc[:, ~df.columns.str.startswith('moe')]
df = df.iloc[:,:-1]

#df.to_csv("race_data_clean.csv")


