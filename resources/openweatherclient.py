from dataclasses import dataclass
from dotenv import load_dotenv
from os import environ

import httpx


WIND_DIRECTIONS = [
    "N",
    "NNE",
    "NE",
    "ENE",
    "E",
    "ESE",
    "SE",
    "SSE",
    "S",
    "SSW",
    "SW",
    "WSW",
    "W",
    "WNW",
    "NW",
    "NNW",
]


def get_cardinal_bearing_from_degrees(degrees: int) -> str:
    # Source: https://gist.github.com/RobertSudwarts #
    ix = int(round(degrees / (360.0 / len(WIND_DIRECTIONS))))
    return WIND_DIRECTIONS[ix % len(WIND_DIRECTIONS)]


@dataclass
class City:
    name: str
    country: str
    state: str
    lat: float
    lon: float


@dataclass
class Weather:
    temp: str
    pressure: str
    humidity: str
    wind_speed: str
    wind_direction: str
    clouds: str
    rain: str
    snow: str


class OpenWeatherClient:
    def __init__(self):
        self._load_api_resources()
        self.weather_client = httpx.Client(base_url=environ["OPENWEATHER_URL"])
        self._units = "metric"

    def _load_api_resources(self) -> None:
        if not load_dotenv():
            raise Exception("Failed to load api resources")

    def get_city_location_data(
        self, city_name: str, limit_listings_to: int
    ) -> list[City]:
        params = {
            "q": f"{city_name}",
            "limit": limit_listings_to,
            "appid": environ["OPENWEATHER_API_TOKEN"],
        }
        response = self.weather_client.get(url="geo/1.0/direct", params=params)
        response.raise_for_status()
        payload = response.json()
        cities = []
        for city in payload:
            cities.append(
                City(
                    name=city["name"],
                    country=city["country"],
                    state=city["state"],
                    lat=city["lat"],
                    lon=city["lon"],
                )
            )
        print(cities)
        return cities

    def get_weather_by_coordinates(self, lat: float, lon: float) -> Weather:
        params = {
            "lat": lat,
            "lon": lon,
            "units": self._units,
            "appid": environ["OPENWEATHER_API_TOKEN"],
        }
        response = self.weather_client.get(url="data/2.5/weather", params=params)
        response.raise_for_status()
        payload = response.json()
        return Weather(
            temp=f'{payload["main"]["temp"]} C',
            pressure=f'{payload["main"]["pressure"]} hPa',
            humidity=f'{payload["main"]["humidity"]} %',
            wind_speed=f'{payload["wind"]["speed"]} m/s',
            wind_direction=f'{get_cardinal_bearing_from_degrees(payload["wind"]["deg"])}',
            clouds=f'{payload["clouds"]["all"]} % chance',
            rain=f'{payload["rain"]["1h"]} mm/h' if "rain" in payload else "no rain",
            snow=f'{payload["snow"]["1h"]} mm/h' if "snow" in payload else "no snow",
        )
