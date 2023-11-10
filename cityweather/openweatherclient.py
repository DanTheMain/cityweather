import httpx
from httpx import QueryParams
from cityweather.schemas import City, Weather

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


class OpenWeatherClient:
    def __init__(self, base_url: str, token: str, units: str):
        self.base_url = base_url
        self._token = token
        self.client = httpx.Client(base_url=self.base_url)
        self.units = units

    def get_city_location_data(
        self, city_name: str, limit_listings_to: int | None = None
    ) -> list[City]:
        params = QueryParams(
            {
                "q": city_name,
                "limit": limit_listings_to,
                "appid": self._token,
            }
        )
        response = self.client.get(url="geo/1.0/direct", params=params)
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
        params = QueryParams(
            {
                "lat": lat,
                "lon": lon,
                "units": self.units,
                "appid": self._token,
            }
        )
        response = self.client.get(url="data/2.5/weather", params=params)
        response.raise_for_status()
        payload = response.json()
        res = Weather(
            temp=f'{payload["main"]["temp"]}C',
            pressure=f'{payload["main"]["pressure"]}hPa',
            humidity=f'{payload["main"]["humidity"]}%',
            wind_speed=f'{payload["wind"]["speed"]}m/s',
            wind_direction=f'{get_cardinal_bearing_from_degrees(payload["wind"]["deg"])}',
            clouds=f'{payload["clouds"]["all"]}% chance',
            rain=f'{payload["rain"]["1h"]} mm/h'
            if "rain" in payload
            else "no rain data",
            snow=f'{payload["snow"]["1h"]} mm/h'
            if "snow" in payload
            else "no snow data",
        )
        return res
