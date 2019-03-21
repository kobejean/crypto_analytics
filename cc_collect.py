import pandas as pd
import json
import requests


url = 'https://min-api.cryptocompare.com/data/histoday'
parameters = {
    'fsym': input('Symbols: '),
    'tsym': input('Convert Symbols: '),
    'limit': input('Limit: ')
}

response = requests.get(url, params=parameters)
data = response.json()
df = pd.DataFrame(data['Data'])
df.to_csv(input('CSV file path: '))
print(df)
#    for item in data['data']:
#        print(item)

