'''
Trying out the API stuff 
'''

import requests


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