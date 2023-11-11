from cityweather.openweatherclient import OpenWeatherClient
from cityweather.schemas import CityWeather


class OpenWeatherService:
    def __init__(self, client: OpenWeatherClient):
        self.client = client
        self.city_name_matches_limit = 5

    def get_city_weather_data(
        self, city_name: str, locations_limit: int | None = None
    ) -> list[CityWeather]:
        payload = self.client.get_city_location_data(
            city_name=city_name,
            limit_listings_to=locations_limit or self.city_name_matches_limit,
        )
        cities = []
        for city in payload:
            city_weather = self.client.get_weather_by_coordinates(city.lat, city.lon)
            cities.append(
                CityWeather(
                    name=city.name,
                    country=city.country,
                    state=city.state,
                    weather=city_weather,
                )
            )
        return cities
