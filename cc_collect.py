import pandas as pd
import json
import requests


daily = 'histoday'
hourly = 'histohour'
minute = 'histominute'

url = 'https://min-api.cryptocompare.com/data/'

interval = input('Interval: ')
if interval == 'daily':
    url += daily
elif interval == 'hourly':
    url += hourly
elif interval == 'minute':
    url += minute
else:
    raise ValueError('Interval must be daily, hourly or minute')

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

