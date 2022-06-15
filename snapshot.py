import sqlite3

import datetime
import sqlite3

from day_type import get_calendar

import requests
from rich import print

import os
from pathlib import Path

if os.path.exists(Path(__file__).parent / 'apikeys.py'):
    from constants import CITIES, PARKINGS_URL
    from apikeys import WARSAW, OPENWEATHER
else:
    with open(Path(__file__).parent / 'apikeys.py', 'w') as f:
        f.write('OPENWEATHER = \nWARSAW = \n')
    print('Please fill out apikeys.py with your API keys first')
    quit()

# Get todays type - working or free
day_type = get_calendar()[datetime.datetime.now().strftime('%Y-%m-%d')]

utc_timestamp = datetime.datetime.utcnow().timestamp()


### Bikes
for city in CITIES:
    # Get fields
    conn = sqlite3.connect(Path(__file__).parent / 'bikes.db')
    # This is used to ensure correct ids land in correct columns.
    # Nextbike API has consistent ordering, but better be prepared for when it changes or we use a different provider.
    cur = conn.execute(f'select * from "{city.name.lower()}"')
    fields = [field[0] for field in cur.description]
    conn.close()

    # Get weather
    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={city.lat}&lon={city.lon}&appid={OPENWEATHER}').json()
    print(weather)

    # Get bikes
    bikes = requests.get(city.bike_url + 'station_status.json').json()['data']['stations']
    for bike in bikes:
        i = fields.index(bike['station_id'])
        fields.insert(i, bike['num_bikes_available'])
        fields.remove(bike['station_id'])
        # ^ This is suprisingly fast
        
    # print(fields)
    fields[0] = utc_timestamp
    fields[1] = day_type
    fields[2] = weather['weather'][0]['main']
    fields[3] = weather['main']['temp']
    fields[4] = weather['wind']['speed']
    fields[5] = weather['clouds']['all']
    fields[6] = weather.get('rain', {}).get('1h', 0)

    conn = sqlite3.connect(Path(__file__).parent / 'bikes.db')
    cur = conn.cursor()
    cur.execute(f'insert into "{city.name.lower()}" values {str(tuple(fields))}')
    conn.commit()
    conn.close()

### Parkings
conn = sqlite3.connect(Path(__file__).parent / 'parkings.db')
cur = conn.cursor()
parkings = requests.get(PARKINGS_URL).json()['result']['Parks']
for parking in parkings:
    entry = (
        utc_timestamp,
        day_type,
        parking['name'],
        parking['free_places_total']['disabled'],
        parking['free_places_total']['public'],
        parking['free_places_total']['electric'],
    )

    cur.execute(f'insert into parkings values {entry}')
    conn.commit()

conn.close()
