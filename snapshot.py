import sqlite3

import datetime
import sqlite3

from apikeys import *
import requests
from rich import print

from constants import CITIES

conn = sqlite3.connect('bikes.db')
# This is used to ensure correct ids land in correct columns.
# Nextrbike API has consistent ordering, but better be prepared for when it changes or we use a different provider.
cur = conn.execute('select * from bikes')
fields = [field[0] for field in cur.description]
conn.close()

utc_timestamp = datetime.datetime.utcnow()

for city in CITIES:
    # weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={city.lat}&lon={city.lon}&appid={OPENWEATHER}').json()
    # print(weather)

    bikes = requests.get(city.bike_url).json()['data']['stations']
    for bike in bikes:
        i = fields.index(bike['station_id'])
        fields.insert(i, bike['num_bikes_available'])
        fields.remove(bike['station_id'])
        # ^ This is suprisingly fast
        
    print(fields)
    quit()