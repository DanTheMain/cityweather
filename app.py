from os import environ
from dotenv import load_dotenv


import uvicorn
from fastapi import FastAPI

from cityweather.service import OpenWeatherService, OpenWeatherClient
from cityweather.schemas import OpenWeatherClientConfig

load_dotenv()
app = FastAPI()
weather_data_provider = OpenWeatherService(
    OpenWeatherClient(
        OpenWeatherClientConfig(
            base_url=environ["OPENWEATHER_URL"],
            token=environ["OPENWEATHER_API_TOKEN"],
        )
    )
)


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
