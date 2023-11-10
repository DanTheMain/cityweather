import pytest
from unittest.mock import patch
import json
from faker import Faker
from random import choice

from cityweather.service import OpenWeatherClient
from cityweather.openweatherclient import City, Weather, WIND_DIRECTIONS

from cityweather.service import OpenWeatherService


fake = Faker()


@pytest.fixture
def cities():
    def inner(num_cities: int | None = None):
        return [
            City(
                name=fake.city(),
                country=f"{fake.first_name()}_country",
                state=f"{fake.first_name()}_state",
                lat=fake.coordinate(),
                lon=fake.coordinate(),
            )
            for _ in range(num_cities or choice(range(1, 10)))
        ]

    return inner


@pytest.fixture
def weather():
    return Weather(
        temp=f"{choice(range(-60, 60))} C",
        pressure=f"{choice(range(1, 1000))} hPa",
        humidity=f"{choice(range(101))}%",
        wind_speed=f"{choice(range(100))} m/s",
        wind_direction=f"{WIND_DIRECTIONS[choice(range(len(WIND_DIRECTIONS)))]}",
        clouds=f"{choice(range(101))}% chance",
        rain=f"{choice(range(1000))} mm/h",
        snow=f"{choice(range(1000))} mm/h",
    )


@pytest.fixture
def mock_open_weather_client():
    return OpenWeatherClient("_", "_", "_")


@pytest.fixture
def mock_open_weather_service(cities, weather, mock_open_weather_client):
    with (
        patch(
            "cityweather.openweatherclient.OpenWeatherClient.get_city_location_data"
        ) as mock_get_city_location_data,
        patch(
            "cityweather.openweatherclient.OpenWeatherClient.get_weather_by_coordinates"
        ) as mock_get_weather_by_coordinates,
    ):
        service = OpenWeatherService(mock_open_weather_client)
        default_num_listings = service.city_name_matches_limit
        mock_get_city_location_data.return_value = cities(default_num_listings)
        mock_get_weather_by_coordinates.return_value = weather

        yield service


@pytest.fixture
def mock_city_data_response():
    payload = [
        {
            "name": "Moscow",
            "local_names": {
                "ku": "Moskow",
                "kl": "Moskva",
            },
            "lat": 55.7504461,
            "lon": 37.6174943,
            "country": "RU",
            "state": "Moscow",
        },
        {
            "name": "Moscow",
            "local_names": {"en": "Moscow", "ru": "Москва"},
            "lat": 46.7323875,
            "lon": -117.0001651,
            "country": "US",
            "state": "Idaho",
        },
        {
            "name": "Moscow",
            "lat": 45.071096,
            "lon": -69.891586,
            "country": "US",
            "state": "Maine",
        },
        {
            "name": "Moscow",
            "lat": 35.0619984,
            "lon": -89.4039612,
            "country": "US",
            "state": "Tennessee",
        },
        {
            "name": "Moscow",
            "lat": 39.5437014,
            "lon": -79.0050273,
            "country": "US",
            "state": "Maryland",
        },
    ]

    response_cities = [
        City(
            name="Moscow", country="RU", state="Moscow", lat=55.7504461, lon=37.6174943
        ),
        City(
            name="Moscow", country="US", state="Idaho", lat=46.7323875, lon=-117.0001651
        ),
        City(name="Moscow", country="US", state="Maine", lat=45.071096, lon=-69.891586),
        City(
            name="Moscow",
            country="US",
            state="Tennessee",
            lat=35.0619984,
            lon=-89.4039612,
        ),
        City(
            name="Moscow",
            country="US",
            state="Maryland",
            lat=39.5437014,
            lon=-79.0050273,
        ),
    ]

    return {
        "payload": json.loads(json.dumps(payload)),
        "city_data": response_cities,
    }


@pytest.fixture
def mock_city_weather_data_response():
    mock_payload = {
        "coord": {"lon": -79.005, "lat": 39.5437},
        "main": {
            "temp": 16.2,
            "feels_like": 16.15,
            "temp_min": 12.16,
            "temp_max": 17.4,
            "pressure": 1011,
            "humidity": 87,
            "sea_level": 1011,
            "grnd_level": 953,
        },
        "visibility": 10000,
        "wind": {"speed": 1.34, "deg": 239, "gust": 2.24},
        "rain": {"1h": 7.95},
        "clouds": {"all": 90},
        "dt": 1699547542,
        "sys": {
            "type": 2,
            "id": 61356,
            "country": "US",
            "sunrise": 1699530784,
            "sunset": 1699567599,
        },
        "timezone": -18000,
        "id": 4361085,
        "name": "Lonaconing",
        "cod": 200,
    }
    mock_weather = Weather(
        temp="16.2C",
        pressure="1011hPa",
        humidity="87%",
        wind_speed="1.34m/s",
        wind_direction="WSW",
        clouds="90% chance",
        rain="7.95 mm/h",
        snow="no snow data",
    )

    return {
        "payload": json.loads(json.dumps(mock_payload)),
        "mock_weather": mock_weather,
    }
