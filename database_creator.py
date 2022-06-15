import json
import os
from constants import CITIES
import sqlite3
from pathlib import Path
import requests

## Bikes
BIKES_URL = 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_vp/pl/station_status.json'

if not os.path.exists(Path(__file__).parent / 'data'):
    os.mkdir(Path(__file__).parent / 'data')

conn = sqlite3.connect(Path(__file__).parent / 'bikes.db')
cur = conn.cursor()

# Download data from gbfs
data = []
for city in CITIES:
    city_data = requests.get(city.bike_url + 'station_status.json').json()['data']['stations']
    # TODO: some freshness check?

    # Create table with columns for every station
    #     in UTC |  DP/SB... | clear, sunny... | Kelvin  |     m/s     |    %    | in mm, last hour
    ids = ['time', 'day_type', 'condition', 'temperature', 'wind_speed', 'clouds', 'rain']
    for st in city_data:
        ids.append(st['station_id'])

    cur.execute(f'''CREATE TABLE "{city.name.lower()}" {str(tuple(ids))}''', )


conn.close()

### P+R
conn = sqlite3.connect(Path(__file__).parent / 'parkings.db')
cur = conn.cursor()
cur.execute(f'''CREATE TABLE parkings (time, day_type, name, disable, public, electric)''', )
conn.commit()
conn.close()
