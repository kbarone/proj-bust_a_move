import pandas as pd

zhvi = pd.read_csv("zillow_home_value_index.csv", index_col = "RegionID")

#zhvi.groupby().filter(lambda x: x.sum() > 2)

