#Equal-Weight S&P 500 Index Fund

#Libary Imports
import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math



#Importing List of Stocks
#Usually you would connect to index provider/financial data API to get list of companies 
stocks = pd.read_csv('sp_500_stocks.csv')

#Acquiring an API token
#Free IEX Cloud API token, free, randomized data
from secrets import IEX_CLOUD_API_TOKEN

#Printing single stock
symbol = 'AAPL'
api_url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url).json()
print(data)
