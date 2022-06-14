from dataclasses import dataclass


BIKES_URL = 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_vp/pl/station_status.json'

@dataclass
class City:
    name: str
    lat: float
    lon: float
    bike_url: str

CITIES = [
    City('Warszawa', 52.228554, 21.011289, 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_vp/pl/station_status.json'),
    City('Pruszków', 52.170110, 20.804862, 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_or/pl/station_status.json'),
    City('Piaseczno', 52.078011, 21.025362, '(https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_pi/pl/station_status.json'),
    City('Otwock', 52.107482, 21.261412, 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_os/pl/station_status.json'),
    City('Grodzisk Mazowiecki', 52.106322, 20.633080, 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_gp/pl/station_status.json'),
    City('Żyrardów', 52.049479, 20.445386, 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_zy/pl/station_status.json'),
]
