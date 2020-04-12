from forecast_api.base_api_forecast import BaseAPIForecast
from forecast_mapper.weather_api_forecast_mapper import WeatherAPIForecastMapper
from request_query_string_parser import RequestQueryStringParser


class StaticAPIForecast(BaseAPIForecast):
    def __init__(self, query_string_parser: RequestQueryStringParser):
        super().__init__(query_string_parser)
        self.request_url = 'resources/weather-api/forecast-singen.json'

    def retrieve_json_string_from_endpoint(self):
        with open(self.request_url, 'r') as forecast_json_file:
            forecast_json_string = forecast_json_file.read()

        return forecast_json_string

    # noinspection Pylint
    def create_mapper(self, json_string):
        return WeatherAPIForecastMapper(json_string)
