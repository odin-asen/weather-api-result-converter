import json

from forecast_api.base_api_forecast import BaseAPIForecast
from request_query_string_parser import RequestQueryStringParser

STATIC_FILES_ROOT = 'resources/weather-api/'


# noinspection Pylint
class StaticAPIForecast(BaseAPIForecast):
    def __init__(self, query_string_parser: RequestQueryStringParser):
        super().__init__(query_string_parser)
        self.request_url = STATIC_FILES_ROOT + 'forecast-singen.json'

    def retrieve_json_from_endpoint(self):
        with open(self.request_url, 'r') as forecast_json_file:
            forecast_json_string = forecast_json_file.read()
            forecast_json = json.loads(forecast_json_string)

        return forecast_json
