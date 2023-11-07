from dataclasses import dataclass


@dataclass
class OpenWeatherClientConfig:
    base_url: str
    token: str


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


@dataclass
class CityWeather:
    name: str
    country: str
    state: str
    weather: Weather
