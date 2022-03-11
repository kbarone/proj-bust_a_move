import pandas as pd
import numpy as np

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
