import json
import requests

from datetime import datetime, timedelta, date

from flask import Flask

app = Flask(__name__)

FORECAST_URL = "http://api.weatherapi.com/v1/forecast.json?key=<klucz__weather_api>"
WA_DATE_FORMAT = "%Y-%m-%d"
WA_FORECAST_KEYS = ['avgtemp_c', 'maxwind_kph', 'avghumidity', 'daily_chance_of_rain']


def get_no_days_apart(date_to):
    today = datetime.combine(date.today(), datetime.min.time())
    td = date_to - today
    no_days = td.days
    if no_days < 0:
        raise ValueError(f"date_to: {date_to} earlier than now: {today}")
    return no_days


def filter_weather_data(resp, date_from, date_to):
    otp = {}
    resp_dict = json.loads(resp.content)
    otp["code"] = resp.status_code
    otp["city_name"] = resp_dict['location']['name']
    otp['lat'] = resp_dict['location']['lat']
    otp['lon'] = resp_dict['location']['lon']
    forecast = resp_dict['forecast']['forecastday']

    for f in forecast:
        print(f"\t{datetime.strptime(f['date'], WA_DATE_FORMAT)}")
    forecast_filtered = [row for row in forecast if date_from <= datetime.strptime(row['date'], WA_DATE_FORMAT)]

    forecast_filtered = [row for row in forecast_filtered if datetime.strptime(row['date'], WA_DATE_FORMAT) <= date_to]
    
    forecast_dict = {}
    for row in forecast_filtered:
        key = row['date']
        data = row['day']
        fc = {}
        for k in WA_FORECAST_KEYS:
            fc[k] = data[k]
        fc['condition'] = data['condition']['text']
        fc['condition_icon'] = data['condition']['icon']
        forecast_dict[key] = fc
    otp['forecast'] = forecast_dict
    return otp


def get_forecast(city_name, date_from, date_to):
    no_days = get_no_days_apart(date_to) + 1  # without the +1 API returns forecast from date_from to date_to - 1 day
    resp = _get_forecast_from_weather_api(city_name, no_days)

    code = resp.status_code

    if code >= 400:  # code 4xx
        output = json.loads(resp.content)
        output['code'] = code
        return output

    return filter_weather_data(resp, date_from, date_to)


def _get_forecast_from_weather_api(query, days):
    txt = remove_polish_letters(query)
    url = FORECAST_URL + f"&q={txt}&days={days}"
    resp = requests.get(url=url)
    return resp


def remove_polish_letters(text):
    return (text.lower()
            .replace('ą', 'a')
            .replace('ć', 'c')
            .replace('e', 'ę')
            .replace('ł', 'l')
            .replace('ń', 'n')
            .replace('ó', 'o')
            .replace('ś', 's')
            .replace('ź', 'z')
            .replace('ż', 'z')
            )


if __name__ == "__main__":
    date_from = datetime.now()
    date_to = date_from + timedelta(days=7)

    resp = get_forecast("Łódź", date_from, date_to)

    print(resp)
    exit()