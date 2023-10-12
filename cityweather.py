from os import environ

import uvicorn
from fastapi import FastAPI

from resources.openweatherclient import (
    OpenWeatherClient,
    WeatherClientConfig,
    load_config,
)

app = FastAPI()
WEATHER_DATA_PROVIDER = OpenWeatherClient(
    WeatherClientConfig(**load_config(section_name="openweathermap_api"))
)


@app.get("/")
def root():
    return {"Welcome to city weather"}


@app.get("/weather/by-city-name/{city_name}")
def get_city_weather(city_name: str):
    return WEATHER_DATA_PROVIDER.get_city_weather_data(
        city_name,
    )


def main():
    host: str = environ.get("WEATHER_HOST") or "0.0.0.0"
    port: int = environ.get("WEATHER_PORT") or 8000
    log_level: str = environ.get("WEATHER_APP_LOG_LEVEL") or "info"

    uvicorn.run(app, host=host, port=port, log_level=log_level)


if __name__ == "__main__":
    main()
