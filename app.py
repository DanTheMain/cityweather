from os import environ
from dotenv import load_dotenv


import uvicorn
from fastapi import FastAPI

from cityweather.service import OpenWeatherService, OpenWeatherClient
from config import load_config

load_dotenv()

config = load_config()
openweather_client = OpenWeatherClient(
    base_url=config.openweather.base_url,
    token=config.openweather.token,
    units=config.openweather.units,
)
weather_data_provider = OpenWeatherService(openweather_client)


app = FastAPI()


@app.get("/weather/{city_name}")
def get_city_weather(city_name: str):
    return weather_data_provider.get_city_weather_data(
        city_name,
    )


if __name__ == "__main__":
    host = environ["WEATHER_HOST"]
    port = environ["WEATHER_PORT"]
    log_level = environ["WEATHER_APP_LOG_LEVEL"]

    uvicorn.run(app, host=host, port=int(port), log_level=log_level)
