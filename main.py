# Equal-Weight S&P 500 Index Fund

# Libary Imports
from secrets import IEX_CLOUD_API_TOKEN
from typing import final
import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math


#Ignore warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



# Importing List of Stocks
# Usually you would connect to index provider/financial data API to get list of companies
stocks = pd.read_csv('sp_500_stocks.csv')
stocks = stocks[~stocks['Ticker'].isin(['DISCA', 'HFC','VIAC','WLTW'])] #Filter out delisted stocks
# Acquiring an API token
# Free IEX Cloud API token, free, randomized data

# Printing single stock
symbol = 'AAPL'
api_url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url).json()
# print(data)

# Parsing API Call, using dictionary to get desired data
price = data['latestPrice']
market_cap = data['marketCap']/1000000000000 #Dividing by 1 trillion to get market cap in trillions
high = data['high']
low = data['low']
# print(price , (market_cap/1000000000000)) 

# Adding Stocks Data to Pandas DataFrame
my_columns = ['Ticker', 'Stock Price', 'Day High', 'Day low',
              'Market Capitalization', 'Number of Shares to Buy']
final_dataframe = pd.DataFrame(columns=my_columns)

#note append will be removed in future panda versions
final_dataframe.append( #only gets result for AAPL
    pd.Series(
        [
            symbol,
            price,
            high,
            low,
            market_cap,
            'N/A'
        ], index=my_columns
    ),
    ignore_index=True
)


"""
Experimenting with concat 

df = pd.concat([
    pd.Series(
        [
            symbol,
            price,
            high,
            low,
            market_cap,c
            'N/A'
        ], index=my_columns
    )
], axis=0
)
"""
#print(final_dataframe)

# Looping through all stocks
final_dataframe = pd.DataFrame(columns=my_columns)

for stock in stocks['Ticker'][:5]:
    api_url = f'https://cloud.iexapis.com/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url).json()
    final_dataframe = final_dataframe.append(
        pd.Series(
            [
                stock,
                data['latestPrice'],
                data['high'],
                data['low'],
                data['marketCap']/1000000000000,
                'N/A'
            ], index=my_columns
        ),
        ignore_index=True
    )

#print(final_dataframe)


#Batch API Call
#using chunks to split into smaller lists
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

symbol_groups = list(chunks(stocks['Ticker'], 100)) #Chunks of 100
symbol_strings = []

for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i])) 
#    print(symbol_strings[i])

final_dataframe = pd.DataFrame(columns=my_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
            pd.Series(
                [
                    symbol,
                    data[symbol]['quote']['latestPrice'],
                    data[symbol]['quote']['high'],
                    data[symbol]['quote']['low'],
                    data[symbol]['quote']['marketCap'],
                    'N/A'
                ], index=my_columns
            ),
            ignore_index=True
        )

print(final_dataframe)
