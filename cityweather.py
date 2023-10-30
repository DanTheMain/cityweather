from os import environ

import uvicorn
from fastapi import FastAPI

from resources.service import OpenWeatherService

app = FastAPI()
weather_data_provider = OpenWeatherService()


@app.get("/weather/{city_name}")
def get_city_weather(city_name: str):
    return weather_data_provider.get_city_weather_data(
        city_name,
    )


if __name__ == "__main__":
    # TODO: figure out how to load .env here
    host = environ["WEATHER_HOST"]
    port = environ["WEATHER_PORT"]
    log_level = environ["WEATHER_APP_LOG_LEVEL"]

    uvicorn.run(app, host=host, port=int(port), log_level=log_level)
