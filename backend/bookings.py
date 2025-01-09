import datetime
import json

import requests

HOTEL_API_URL = "https://api.content.tripadvisor.com/api/v1/location/nearby_search"

with open('./backend/config.json', 'r+') as file:
    config = json.load(file)


def get_accommodation_data(lat, lon):
    data = {
        "key": config["TRIPADVISOR_API_KEY"],
        "latLong": f"{lat},{lon}",
        "category": "hotels"
    }
    response = requests.get(url=HOTEL_API_URL, params=data)
    code = response.status_code
    resp = response.json()

    if code >= 400:  # code 4xx
        output = json.loads(resp.content)
        output['code'] = code
        return output
    output = resp
    output['code'] = code
    return output


def get_single_location_data(location_id):
    LOCATION_DETAILS_URL = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/details"
    data = {
        "key": config["TRIPADVISOR_API_KEY"],
        "language": "en",
        "currency": "USD"
    }
    headers = {"accept": "application/json"}

    response = requests.get(url=LOCATION_DETAILS_URL, params=data, headers=headers)
    resp = response.json()
    if response.status_code >= 400:  # code 4xx
        output = resp
        output['code'] = response.status_code
        return output
    result = {}
    result['code'] = response.status_code
    result['location_id'] = resp['location_id']
    result["name"] = resp["name"]
    result["web_url"] = resp["web_url"]
    result["address_obj"] = resp["address_obj"]
    result["rating"] = resp["rating"] if "rating" in resp else "brak"
    result["price_level"] = resp["price_level"] if "price_level" in resp else "brak"
    # print(response.text)
    return result

def get_location_ids(bookings_data):
    ids = []
    for entry in bookings_data['data']:
        ids.append(entry['location_id'])
    return ids

def get_all_location_data(bookings_data):
    ids = get_location_ids(bookings_data)
    all_location_data = []
    for id in ids:
        single_location_data = get_single_location_data(id)
        all_location_data.append(single_location_data)
    
    return all_location_data


if __name__ == '__main__':
    from weather import get_forecast
    data = get_forecast("Konin", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=5))
    pass
    # print(data)
    # booking_data = get_accommodation_data(data['lat'], data['lon'])

    booking_data = get_accommodation_data("test", "test")
    print(booking_data)

    result = get_single_location_data(booking_data['data'][0]['location_id'])
    print(result)
    # result = get_single_location_data('dfvjyhsabfjsnm1234567')
    # print(result)
