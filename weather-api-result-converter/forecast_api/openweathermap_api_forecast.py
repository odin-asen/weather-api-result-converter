from forecast_api.base_api_forecast import BaseAPIForecast, read_api_key_from_config
from forecast_mapper.base_forecast_mapper import BaseForecastMapper
from forecast_mapper.openweathermap_api_forecast_mapper import OpenweathermapAPIForecastMapper
from request_query_string_parser import RequestQueryStringParser


class OpenweathermapAPIForecast(BaseAPIForecast):
    def __init__(self, query_string_parser: RequestQueryStringParser, use_static_file=False):
        super().__init__(query_string_parser)
        self.use_static_file = use_static_file
        self.static_file_path = '../resources/openweathermap/onecall-beuren.json'
        if not use_static_file:
            if not query_string_parser.has_search_query():
                raise ValueError('Query string contains insufficient set of values. '
                                 'OpenweathermapAPIForecast requires search query')

    def make_forecast_url(self):
        url_base = 'http://api.openweathermap.org/data/2.5/onecall'
        lat_lon = self.query_string_parser.retrieve_search_query().split(',', 2)
        return url_base + '?appid={api_key}&lat={lat}&lon={lon}&mode=json&units=metric'.format(
            api_key=read_api_key_from_config('openweathermap'),
            lat=lat_lon[0],
            lon=lat_lon[1]
        )

    # noinspection Pylint
    def create_mapper(self, json_string) -> BaseForecastMapper:
        return OpenweathermapAPIForecastMapper(json_string)

    @property
    def get_api_name(self) -> str:
        return 'openweathermap'
