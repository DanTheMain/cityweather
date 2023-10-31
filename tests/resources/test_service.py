from faker import Faker
import pytest
from unittest.mock import patch, Mock
from random import choice

import resources.openweatherclient
from resources.service import OpenWeatherService, CityWeather
from resources.openweatherclient import City, Weather, WIND_DIRECTIONS


fake = Faker()


@pytest.fixture
def generate_cities(num_cities: int = 5):
    return [
        City(
            name=fake.city(),
            country=f"{fake.first_name()}_country",
            state=f"{fake.first_name()}_state",
            lat=fake.coordinate(),
            lon=fake.coordinate(),
        )
        for _ in range(num_cities)
    ]


@pytest.fixture
def generate_weather():
    return Weather(
        temp=f"{choice(range(-60, 60))} C",
        pressure=f"{choice(range(1, 1000))} hPa",
        humidity=f"{choice(range(101))} %",
        wind_speed=f"{choice(range(100))} m/s",
        wind_direction=f"{WIND_DIRECTIONS[choice(range(len(WIND_DIRECTIONS)))]}",
        clouds=f"{choice(range(101))} % chance",
        rain=f"{choice(range(1000))} mm/h",
        snow=f"{choice(range(1000))} mm/h",
    )


def test__service_get_city_weather_data__returns_expected_weather(
    generate_cities,
    generate_weather,
):
    with (
        patch(
            "resources.openweatherclient.OpenWeatherClient.get_city_location_data"
        ) as mock_get_city_location_data,
        patch(
            "resources.openweatherclient.OpenWeatherClient.get_weather_by_coordinates"
        ) as mock_get_weather_by_coordinates,
    ):
        mock_get_city_location_data.return_value = generate_cities
        mock_get_weather_by_coordinates.return_value = generate_weather
        assert (
            OpenWeatherService().get_city_weather_data("test_city", 1)[0].weather
            == generate_weather
        )
