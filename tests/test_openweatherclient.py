import pytest
import httpx

from cityweather.openweatherclient import (
    get_cardinal_bearing_from_degrees,
    OpenWeatherClient,
)


BASE_MOCK_URL = "https://fake.url"


@pytest.mark.parametrize(
    "degree, direction",
    [
        (0, "N"),
        (1, "N"),
        (25, "NNE"),
        (33, "NNE"),
        (34, "NE"),
        (56, "NE"),
        (57, "ENE"),
        (57, "ENE"),
        (78, "ENE"),
        (79, "E"),
        (101, "E"),
        (102, "ESE"),
        (123, "ESE"),
    ],
)
def test__get_cardinal_bearing_from_degrees__returns_expected_directions_for_edge_values(
    degree: int, direction: str
):
    assert get_cardinal_bearing_from_degrees(degree) == direction


@pytest.mark.respx(base_url=BASE_MOCK_URL)
def test__client_get_weather_by_coordinates__raises_not_found_response(respx_mock):
    respx_mock.get("data/2.5/weather").mock(return_value=httpx.Response(404))
    mock_client = OpenWeatherClient(BASE_MOCK_URL, "_", "_")

    with pytest.raises(httpx.HTTPStatusError):
        assert mock_client.get_weather_by_coordinates(0, 0)


@pytest.mark.respx(base_url=BASE_MOCK_URL)
def test__client_get_city_location_data__raises_not_found_response(respx_mock):
    respx_mock.get("geo/1.0/direct").mock(return_value=httpx.Response(404))
    mock_client = OpenWeatherClient(BASE_MOCK_URL, "_", "_")

    with pytest.raises(httpx.HTTPStatusError, match="404"):
        assert mock_client.get_city_location_data("_")


def test__get_city_location_data__responds_with_expected_city_data_listings(
    respx_mock, mock_city_data_response
):
    expected_response = httpx.Response(
        status_code=200, json=mock_city_data_response["payload"]
    )
    respx_mock.get("geo/1.0/direct").mock(return_value=expected_response)
    mock_client = OpenWeatherClient(BASE_MOCK_URL, "_", "_")

    assert (
        mock_client.get_city_location_data("_", 5) == mock_city_data_response["city_data"]
    )


@pytest.mark.respx(base_url=BASE_MOCK_URL)
def test__client_get_weather_by_coordinates__responds_with_expected__weather_data(
    respx_mock, mock_city_weather_data_response
):
    expected_response = httpx.Response(
        status_code=200, json=mock_city_weather_data_response["payload"]
    )
    respx_mock.get("data/2.5/weather").mock(return_value=expected_response)
    mock_client = OpenWeatherClient(BASE_MOCK_URL, "_", "_")
    assert (
        mock_client.get_weather_by_coordinates(0, 0)
        == mock_city_weather_data_response["mock_weather"]
    )
