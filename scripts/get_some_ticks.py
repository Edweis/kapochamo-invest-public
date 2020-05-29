import requests
import pandas as pd

base_url = 'https://api.binance.com/api/v3'
parameters = {
    'symbol': 'BTCUSDT',
    'limit': 1000,
    'interval': '1m',
    'startTime': 1587271070010, # Convert to human time there : https://www.epochconverter.com/
}
columns = [
    'open_time',
'open',
'high',
'low',
'close',
'volume',
'close_time',
'quote_asset_volume',
'number_of_trades',
'taker_buy_base_asset_volume',
'taker_buy_quote_asset_volume',
'ignore',
]

response = requests.get(base_url+'/klines', parameters)
assert response.status_code == 200 # Check that is worked well

first_1000_ticks = response.json()
print(first_1000_ticks)

df = pd.DataFrame.from_records(first_1000_ticks, columns=columns)
df.head()



