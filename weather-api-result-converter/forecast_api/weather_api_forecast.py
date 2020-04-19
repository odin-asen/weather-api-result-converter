from forecast_api.base_api_forecast import BaseAPIForecast, read_api_key_from_config
from forecast_mapper.base_forecast_mapper import BaseForecastMapper
from forecast_mapper.weather_api_forecast_mapper import WeatherAPIForecastMapper
from request_query_string_parser import RequestQueryStringParser


class WeatherAPIForecast(BaseAPIForecast):
    def __init__(self, query_string_parser: RequestQueryStringParser, use_static_file=False):
        super().__init__(query_string_parser)
        self.use_static_file = use_static_file
        self.static_file_path = 'weather-api/forecast-singen.json'
        if not use_static_file:
            if not query_string_parser.has_search_query():
                raise ValueError('Query string contains insufficient set of values. '
                                 'WeatherAPIForecast requires a search query')

    def make_forecast_url(self):
        return 'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={query}&days={days:d}' \
            .format(
                api_key=read_api_key_from_config('weather_api'),
                query=self.query_string_parser.retrieve_search_query(),
                days=self.query_string_parser.retrieve_requested_days()
            )

    # noinspection Pylint
    def create_mapper(self, json_string) -> BaseForecastMapper:
        return WeatherAPIForecastMapper(json_string)

    def get_api_name(self) -> str:
        return 'weather_api'
