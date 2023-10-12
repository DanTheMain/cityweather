import configparser
import json
from dataclasses import dataclass
from pathlib import Path

import httpx

CONFIG_FILE = Path(Path(__file__).parent.absolute(), "config.properties")

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


def _check_config_items(items: dict) -> None:
    if not items:
        raise ValueError("Empty config")
    no_value_keys = [key for key in items.keys() if not items[key]]
    if no_value_keys:
        raise ValueError(
            f"Failed to read config for the following item(s): {no_value_keys}"
        )


def load_config(section_name: str, config_filepath: Path = CONFIG_FILE) -> dict:
    config = configparser.ConfigParser()
    if not config.read(config_filepath):
        raise FileNotFoundError(f"config file not found at {config_filepath}")
    items = dict(config.items(section=section_name))
    _check_config_items(items)
    return items


@dataclass
class WeatherClientConfig:
    scheme: str
    domain: str
    app_key: str
    city_data_dir: str
    loc_weather_dir: str


def get_cardinal_bearing_from_degrees(degrees: int) -> str:
    # Source: https://gist.github.com/RobertSudwarts #
    ix = int(round(degrees / (360.0 / len(WIND_DIRECTIONS))))
    return WIND_DIRECTIONS[ix % len(WIND_DIRECTIONS)]


def filter_weather_data(data: dict) -> dict:
    return {
        "temp": f'{data.get("main").get("temp")} C',
        "pressure": f'{data.get("main").get("pressure")} hPa',
        "humidity": f'{data.get("main").get("humidity")} %',
        "wind speed": f'{data.get("wind").get("speed")} m/s',
        "wind_direction": f'{get_cardinal_bearing_from_degrees(data.get("wind").get("deg"))}',
        "clouds": f'{data.get("clouds").get("all")} %',
        "rain": f'{data.get("rain").get("1h")} mm/h' if "rain" in data else "no rain",
        "snow": f'{data.get("snow").get("1h")} mm/h' if "snow" in data else "no snow",
    }


class OpenWeatherClient:
    def __init__(self, client_config: WeatherClientConfig):
        self._config: WeatherClientConfig = client_config
        self._weather_client: httpx.Client = httpx.Client()
        self._city_name_matches_limit: int = 5
        self._units: str = "metric"

    def _get_data_from_subdir_by_params(self, subdir: str, params: dict) -> json:
        base_url = "/".join(
            [
                self._config.scheme,
                self._config.domain,
                subdir,
            ]
        )
        return self._weather_client.get(base_url, params=params).json()

    def get_city_location_data(self, city_name: str, limit_listings_to) -> json:
        params = {
            "q": f"{city_name}",
            "limit": limit_listings_to,
            "appid": self._config.app_key,
        }
        return self._get_data_from_subdir_by_params(self._config.city_data_dir, params)

    def get_weather_by_coordinates(self, lat: float, lon: float) -> json:
        params = {
            "lat": f"{lat}",
            "lon": lon,
            "units": self._units,
            "appid": self._config.app_key,
        }
        return self._get_data_from_subdir_by_params(
            self._config.loc_weather_dir, params
        )

    def get_city_weather_data(
        self, city_name: str, locations_limit: int | None = None
    ) -> json:
        city_data = self.get_city_location_data(
            city_name=city_name,
            limit_listings_to=locations_limit or self._city_name_matches_limit,
        )
        data = []
        for location in city_data:
            data.append(
                {
                    "name": location["name"],
                    "country": location["country"],
                    "state": location["state"],
                    "weather_data": filter_weather_data(
                        self.get_weather_by_coordinates(
                            location["lat"], location["lon"]
                        )
                    ),
                }
            )
        return data
