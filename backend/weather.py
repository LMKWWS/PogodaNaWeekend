import json
import requests

from datetime import datetime, timedelta, date

from flask import Flask

app = Flask(__name__)

FORECAST_URL = "http://api.weatherapi.com/v1/forecast.json?key=0c41ea7daf794a90bcc202948241412"
WA_DATE_FORMAT = "%Y-%m-%d"
WA_FORECAST_KEYS = ['avgtemp_c', 'maxwind_kph', 'avghumidity', 'daily_chance_of_rain']


@app.route("/")
def hello():
    forecast = get_forecast(query="Łódź", days=14)
    print("My forecast:")
    print(forecast)
    return f"""Hello, World!\n{forecast.text}"""


def get_available_bookings(city_name, date_from, date_to, price_from, price_to):
    pass


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
    otp["city_name"] = resp_dict['location']['name']
    forecast = resp_dict['forecast']['forecastday']
    # for k in forecast:
        # print(k['date'])
    print(date_from)
    print(date_to)
    for f in forecast:
        print(f"\t{datetime.strptime(f['date'], WA_DATE_FORMAT)}")
    forecast_filtered = [row for row in forecast if date_from <= datetime.strptime(row['date'], WA_DATE_FORMAT)]
    print(len(forecast_filtered))
    forecast_filtered = [row for row in forecast_filtered if datetime.strptime(row['date'], WA_DATE_FORMAT) <= date_to]

    forecast_filtered = forecast
    print(len(forecast_filtered))
    
    forecast_dict = {}
    for row in forecast_filtered:
        # print(row)
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
    print(no_days)
    resp = _get_forecast_from_weather_api(city_name, no_days)
    print(date_to)
    return filter_weather_data(resp, date_from, date_to)


def _get_forecast_from_weather_api(query, days):
    txt = remove_polish_letters(query)
    url = FORECAST_URL + f"&q={txt}&days={days}"
    print(url)
    resp = requests.get(url=url)
    resp.raise_for_status()
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
    # app.run()
    date_from = datetime.now()
    date_to = date_from + timedelta(days=2)

    resp = get_forecast("Łódź", date_from, date_to)

    print(resp)
    exit()

    print(type(resp))
    x = resp.content
    print(type(x))
    data = json.loads(x)
    print(type(data))
    print(data.keys())
    print(data['location'])
    print(data['current'])
    forecast = data['forecast']
    print(type(forecast))
    print(forecast.keys())
    forecastday = forecast['forecastday']
    print(type(forecastday))
    print(len(forecastday))
    item = forecastday[0]
    print(type(item))
    print(item.keys())
    forecast_date = item['date']
    fc = item['day']
    print(fc.keys())
    for k, v in fc.items():
        print(f"{k}:\t{v}")