import json

import sqlite3
import requests

BIKES_URL = 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_vp/pl/station_status.json'

conn = sqlite3.connect('bikes.db')
cur = conn.cursor()

# Download data from gbfs
data = requests.get(BIKES_URL)
data.raise_for_status()
data = data.json()['data']['stations']
# TODO: some freshness check?

# Create table with columns for every station
#     in UTC |  DP/SB... | clear, sunny... | Kelvin  |     m/s     |    %    | in mm, last hour
ids = ['time', 'day_type', 'condition', 'temperature', 'wind_speed', 'clouds', 'rain']
for st in data:
    ids.append(st['station_id'])

cur.execute(f'''CREATE TABLE bikes {str(tuple(ids))}''', )
conn.close()
