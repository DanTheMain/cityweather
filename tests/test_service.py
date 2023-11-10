from unittest.mock import patch
from cityweather.service import OpenWeatherService


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
    mock_open_weather_service,
):
    returned_listings = mock_open_weather_service.get_city_weather_data("_")

    assert len(returned_listings) == mock_open_weather_service.city_name_matches_limit
