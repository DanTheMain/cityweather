from unittest.mock import patch
from cityweather.service import OpenWeatherService


def test__service_get_city_weather_data__returns_expected_weather(
    make_cities, weather, mock_open_weather_client
):
    with (
        patch(
            "cityweather.openweatherclient.OpenWeatherClient.get_city_location_data"
        ) as mock_get_city_location_data,
        patch(
            "cityweather.openweatherclient.OpenWeatherClient.get_weather_by_coordinates"
        ) as mock_get_weather_by_coordinates,
    ):
        make_cities = make_cities(1)
        mock_get_city_location_data.return_value = cities
        mock_get_weather_by_coordinates.return_value = weather

        actual_weather = (
            OpenWeatherService(mock_open_weather_client)
            .get_city_weather_data("_", 1)[0]
            .weather
        )

        assert actual_weather == weather


def test__get_city_weather_data__returns_no_weather_with_empty_cities_listings(
    make_cities, weather, mock_open_weather_client
):
    with patch(
        "cityweather.openweatherclient.OpenWeatherClient.get_city_location_data"
    ) as mock_get_city_location_data:
        mock_get_city_location_data.return_value = []

        assert (
            OpenWeatherService(mock_open_weather_client).get_city_weather_data("_", 1)
            == []
        )


def test__get_city_weather_data__returns_full_weather_data_without_locations_limit(
    open_weather_service, city_name, make_cities, weather
):
    open_weather_service.client.get_city_location_data.return_value = make_cities(
        num_cities=10
    )
    open_weather_service.client.get_weather_by_coordinates.return_value = weather

    open_weather_service.get_city_weather_data(city_name)

    assert open_weather_service.client.get_city_location_data.call_count == 1
    call_kwargs = open_weather_service.client.get_city_location_data.call_args.kwargs

    assert call_kwargs["limit_listings_to"] == open_weather_service.city_name_matches_limit

