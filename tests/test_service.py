from faker import Faker
import pytest
from unittest.mock import patch
from random import choice

from cityweather.service import OpenWeatherService, OpenWeatherClient
from cityweather.openweatherclient import City, Weather, WIND_DIRECTIONS


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


def test__service_get_city_weather_data__returns_expected_weather(
    cities, weather, mock_open_weather_client
):
    with (
        patch(
            "cityweather.openweatherclient.OpenWeatherClient.get_city_location_data"
        ) as mock_get_city_location_data,
        patch(
            "cityweather.openweatherclient.OpenWeatherClient.get_weather_by_coordinates"
        ) as mock_get_weather_by_coordinates,
    ):
        cities = cities(1)
        mock_get_city_location_data.return_value = cities
        mock_get_weather_by_coordinates.return_value = weather

        actual_weather = (
            OpenWeatherService(mock_open_weather_client)
            .get_city_weather_data("_", 1)[0]
            .weather
        )

        assert actual_weather == weather


def test__service_get_city_weather_data__returns_no_weather_with_empty_cities_listings(
    cities, weather, mock_open_weather_client
):
    with patch(
        "cityweather.openweatherclient.OpenWeatherClient.get_city_location_data"
    ) as mock_get_city_location_data:
        mock_get_city_location_data.return_value = []

        assert (
            OpenWeatherService(mock_open_weather_client).get_city_weather_data("_", 1)
            == []
        )


def test__service_get_city_weather_data__returns_default_number_of_weather_listings_with_default_locations_limit(
    cities, weather, mock_open_weather_client
):
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

        assert len(service.get_city_weather_data("_")) == default_num_listings
