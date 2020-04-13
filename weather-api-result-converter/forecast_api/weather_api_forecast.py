import requests

from forecast_api.base_api_forecast import BaseAPIForecast
from forecast_mapper.base_forecast_mapper import BaseForecastMapper
from forecast_mapper.weather_api_forecast_mapper import WeatherAPIForecastMapper
from request_query_string_parser import RequestQueryStringParser


class WeatherAPIForecast(BaseAPIForecast):
    def __init__(self, query_string_parser: RequestQueryStringParser, use_static_file=False):
        super().__init__(query_string_parser)
        self.use_static_file = use_static_file
        if not use_static_file:
            if not query_string_parser.has_api_key() or not query_string_parser.has_search_query():
                raise ValueError('Query string contains insufficient set of values. '
                                 'WeatherAPIForecast requires api key and search query')

    def retrieve_json_string_from_endpoint(self):
        if self.use_static_file:
            static_file_path = 'resources/weather-api/forecast-singen.json'
            with open(static_file_path, 'r') as forecast_json_file:
                return forecast_json_file.read()
        else:
            response = requests.get(self.make_forecast_url())
            if response.status_code == 200:
                return response.text

            raise ValueError('Endpoint did not return OK, instead:', response, response.text)

    def make_forecast_url(self):
        return 'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={query}&days={days:d}'\
            .format(
                api_key=self.query_string_parser.retrieve_api_key(),
                query=self.query_string_parser.retrieve_search_query(),
                days=self.query_string_parser.retrieve_requested_days()
            )

    # noinspection Pylint
    def create_mapper(self, json_string) -> BaseForecastMapper:
        return WeatherAPIForecastMapper(json_string)
