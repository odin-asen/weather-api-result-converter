import requests

from forecast_api.base_api_forecast import BaseAPIForecast
from forecast_mapper.base_forecast_mapper import BaseForecastMapper
from forecast_mapper.openweathermap_api_forecast_mapper import OpenweathermapAPIForecastMapper
from request_query_string_parser import RequestQueryStringParser


class OpenweathermapAPIForecast(BaseAPIForecast):
    def __init__(self, query_string_parser: RequestQueryStringParser, use_static_file=False):
        super().__init__(query_string_parser)
        self.use_static_file = use_static_file
#        if not use_static_file:
#            print(query_string_parser.retrieve_api_key())
#            print(query_string_parser.retrieve_search_query())
#            if not query_string_parser.has_api_key() and not query_string_parser.has_search_query():
#                raise ValueError('Query string contains insufficient set of values. '
#                                 'OpenweathermapAPIForecast requires api key and search query')

    def retrieve_json_string_from_endpoint(self):
        if self.use_static_file:
            static_file_path = 'resources/openweathermap/forecast-beuren.json'
            with open(static_file_path, 'r') as forecast_json_file:
                return forecast_json_file.read()
        else:
            response = requests.get(self.make_forecast_url())
            if response.status_code == 200:
                return response.text

            raise ValueError('Endpoint did not return OK, instead:', response, response.text)

    def make_forecast_url(self):
        url_base = 'http://api.openweathermap.org/data/2.5/forecast'
        url = url_base + '?appid={api_key}&q=Singen,de&mode=json&units=metric'.format(
            api_key=self.query_string_parser.retrieve_api_key()
 #           query=self.query_string_parser.retrieve_search_query()
        )
        return url

    # noinspection Pylint
    def create_mapper(self, json_string) -> BaseForecastMapper:
        return OpenweathermapAPIForecastMapper(json_string)
