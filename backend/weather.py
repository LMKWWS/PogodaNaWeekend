import requests

from flask import Flask

app = Flask(__name__)

FORECAST_URL = "http://api.weatherapi.com/v1/forecast.json?key=0c41ea7daf794a90bcc202948241412"


@app.route("/")
def hello():
    forecast = get_forecast(query="Gdańsk", days=14)
    print("My forecast:")
    print(forecast)
    return f"""Hello, World!\n{forecast.text}"""


def get_forecast(query, days):
    url = FORECAST_URL + f"&q={query}&days={days}"
    data = requests.get(url=url)
    print(query, days)
    print(data.text)
    data.raise_for_status()
    return data


if __name__ == "__main__":
    app.run()