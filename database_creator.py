import json
import os
from constants import CITIES
import sqlite3
import requests

BIKES_URL = 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_vp/pl/station_status.json'
os.mkdir('data')

conn = sqlite3.connect('bikes.db')
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
