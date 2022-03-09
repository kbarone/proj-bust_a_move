
import numpy as np
import pandas as pd

c_pop = pd.read_csv("county_population.csv", encoding = "ISO-8859-1", dtype={"STATE" : object, "COUNTY":object, "DIVISION": object})
c_pop = c_pop.rename(columns=str.lower)

c_pop['state'] = c_pop['state'].str.zfill(2)
c_pop['county'] = c_pop['county'].str.zfill(3)

c_pop = c_pop[c_pop['county'] != '000']

womp = pd.read_csv("womply_city_daily.csv")
