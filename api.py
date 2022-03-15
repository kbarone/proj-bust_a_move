'''
Trying out the API stuff 
'''

import requests
import io
import pandas as pd



zillow = "https://api.bridgedataoutput.com/api/v2/zgecon/cut?access_token=91d62741f0adc2b89799df25bcc9299e&regionTypeID=1&metricTypeKey=ZRI"

response = requests.get(zillow) # This will return 401 as we do not have access 
# UPDATE : Zillow allows use of its API only for commercial purposes. 

mashvisor = "https://api.mashvisor.com/v1.1/client/city/list?state=FL"
headers = {"x-api-key" : "9c5e3fd0-d418-4619-b533-8c812c354740"}

mashvisor2 = "https://api.mashvisor.com/v1.1/client/rental-rates?city=Chicago&state=IL&zip_code=60615&source=airbnb"

mashvisor3 = "https://api.mashvisor.com/v1.1/client/neighborhood/268201/historical/airbnb?average_by=revenue&state=CA" #historical data by month

response = requests.get(mashvisor3, headers=headers)

response.text

mashvisor4 = "https://api.mashvisor.com/v1.1/client/city/neighborhoods/{state}/{city}" # this is to get the neighborhoods list to
# use in the API calls that involve neighborhood

mashvisor4 = "https://api.mashvisor.com/v1.1/client/city/neighborhoods/CA/Los%20Angeles" 

mashvisor5 = "https://api.mashvisor.com/v1.1/client/neighborhood/7877/historical/airbnb?average_by=revenue&state=CA"

mashvisor6 = "https://api.mashvisor.com/v1.1/client/neighborhood/7877/historical/airbnb?&state=CA"

census1 = "https://api.census.gov/data/2019/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=2a3bf1bd5b110158358335717d5d067b0e377810"

census2 = "https://api.census.gov/data/timeseries/poverty/saipe?get=SAEMHI_PT,SAEPOVRTALL_PT,NAME&for=county:*&in=state:*&time=2020&key=2a3bf1bd5b110158358335717d5d067b0e377810"

rawData = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
rawData = rawData.rename(columns= {'[["SAEMHI_PT"':"med_inc","SAEPOVRTALL_PT" : "pov_rate","NAME":"county","county]":"fips_county"})
df = rawData.copy()
#df = df.iloc[:,:5]
#df['med_inc'] = df['med_inc'].str.replace("[","")

cols_to_fix = ["med_inc", "fips_county"]
for col in cols_to_fix:
    df[col] = df[col].str.replace("[","")
    df[col] = df[col].str.replace("]","")
    df[col] = df[col].str.replace('"',"")
