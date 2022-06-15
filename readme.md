# Data collector for GBFS and Warsaws parkings along with weather and day type
Collects `available_bikes` from GBFS for every station along with weather data. See `constants.py` to add your own city, and `database creator.py` to see what data it collects. It will create new table for each city you add to `CITIES`.

## Usage
Run `database_creator.py` once, then schedule `snapshot.py` as a cronjob (eg. every 15 minutes)
First time you run `snapshot.py` an `apikeys.py` file will be created. Fill it with your apikeys for openweather and api.um.warszawa.pl

## Motivation
I wanted to do predictive routing for my public bike router and needed info about bike availibility along with weather condition and day type (working/free) in order to better predict amount of bikes.

As for parkings, I was just curious and included it in here as well. It might be disconnected from here someday.

## Data sources
See data sources in `constants.py`
