from dataclasses import dataclass
from os import environ


@dataclass
class OpenWeatherClientConfig:
    base_url: str
    token: str
    units: str


@dataclass
class Config:
    openweather: OpenWeatherClientConfig


def load_config() -> Config:
    openweather = OpenWeatherClientConfig(
        base_url=environ["OPENWEATHER_URL"],
        token=environ["OPENWEATHER_API_TOKEN"],
        units="metric",
    )
    return Config(openweather=openweather)
