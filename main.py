# Импортируем модуль os для работы с переменными окружения
from os import getenv

import dateutil.parser as datetime_parser
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from geopy.geocoders import Nominatim

app = Flask(__name__)

load_dotenv()

geolocation = Nominatim(user_agent="Teva")


@app.route("/v1/forecast/")
def get_forecast():
    # Получаем параметр dt из запроса
    if request.args.get("dt") is None:
        return "Invalid parameter: Datetime parameter is empty"

    try:
        # Пытаемся преобразовать параметр dt в объект datetime
        dt = datetime_parser.parse(request.args.get("dt"))
    except datetime_parser._parser.ParserError:
        return "Invalid parameter: Datetime parameter format is incorrerct. Try something like 2023-03-17T11"

    # Получаем параметр city из запроса
    city = request.args.get("city")
    if city is None:
        return "Invalid parameter: City parameter is empty"

    # Получаем координаты города по его названию с помощью геолокатора
    coord = geolocation.geocode(city)
    if coord is None:
        return "Invalid parameter: City parameter does not represent city name"

    get_param ={
        "latitude": coord.latitude,
        "longitude": coord.longitude,
        "start_date": dt.date(),
        "end_date": dt.date(),
        "hourly": "temperature_2m"
    }

     # Делаем запрос к API погоды 
    response = requests.get(getenv("API"), params=get_param, timeout=30)

    if response.status_code != 200:
        return "Invalid request: Something went wrong while getting response from weather API"

    json_response = response.json()

    return jsonify({"city": city, "unit": "celsius", "temperature": json_response["hourly"]["temperature_2m"][dt.hour]})


@app.route("/v1/current/")
def get_current():
    # Получаем параметр city из запроса
    city = request.args.get("city")
    if city is None:
        return "Invalid parameter: City parameter is empty"

    # Получаем координаты города по его названию с помощью геолокатора
    coord = geolocation.geocode(city)
    if coord is None:
        return "Invalid parameter:City parameter does not represent city name"
    get_param ={
        "latitude": coord.latitude,
        "longitude": coord.longitude,
        "current_weather": "true"
    }

    # Делаем запрос к API погоды
    response = requests.get(getenv("API"), params=get_param, timeout=30)
    if response.status_code != 200:
        return "Invalid request: Something went wrong while getting response from weather API"

    json_response = response.json()

    return jsonify({"city": city, "unit": "celsius", "temperature": json_response["current_weather"]["temperature"]})


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=getenv("PORT"))
