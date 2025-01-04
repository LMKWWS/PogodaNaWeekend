import datetime
import json

import requests

HOTEL_API_URL = "https://api.content.tripadvisor.com/api/v1/location/nearby_search"

with open('config.json', 'r+') as file:
    config = json.load(file)


def get_accommodation_data(lat, lon):
    data = {
        "key": config["TRIPADVISOR_API_KEY"],
        "latLong": f"{lat},{lon}",
        "category": "hotels"
    }
    response = requests.get(url=HOTEL_API_URL, params=data)
    response.raise_for_status()
    resp = response.json()
    for item in resp['data']:
        print(item)


if __name__ == '__main__':
    from weather import get_forecast
    data = get_forecast("Konin", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=5))

    get_accommodation_data(data['lat'], data['lon'])
