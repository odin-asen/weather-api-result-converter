import json
from abc import abstractmethod

import dicttoxml
import requests

from forecast_mapper.base_forecast_mapper import BaseForecastMapper
from request_query_string_parser import RequestQueryStringParser


def read_api_key_from_config(name):
    with open('../config.json', 'r') as config_json:
        return json.loads(config_json.read())['keys'][name]


class BaseAPIForecast:
    def __init__(self, query_string_parser: RequestQueryStringParser):
        self.query_string_parser = query_string_parser
        self.use_static_file = False
        self.static_file_path = ''

    def fetch_and_map_response_as_string(self) -> str:
        forecast_json = self.retrieve_json_string_from_endpoint()

        mapper = self.create_mapper(forecast_json)
        mapped_dictionary = mapper.to_output_dictionary()

        file_format = self.query_string_parser.retrieve_file_format()
        if file_format == 'json':
            return json.dumps(mapped_dictionary, indent=4)

        if file_format == 'xml':
            xml_bytes = dicttoxml.dicttoxml(mapped_dictionary, root=False)
            return xml_bytes.decode('utf-8')

        raise NotImplementedError('Unknown output format {format} not implemented'
                                  .format(format=file_format))

    def retrieve_json_string_from_endpoint(self) -> str:
        if self.use_static_file:
            return self.read_static_json_from_resources()

        response = requests.get(self.make_forecast_url())
        if response.status_code == 200:
            return response.text

        raise ValueError('Endpoint did not return OK, instead:',
                         response, response.text, self.make_forecast_url())

    def read_static_json_from_resources(self) -> str:
        with open('resources/' + self.static_file_path, 'r') as json_file:
            return json_file.read()

    def make_content_type(self) -> str:
        return 'Content-type: application/{file_format}; charset=utf-8'\
            .format(file_format=self.query_string_parser.retrieve_file_format())

    @abstractmethod
    def create_mapper(self, json_string: str) -> BaseForecastMapper:
        pass

    @abstractmethod
    def get_api_name(self) -> str:
        pass

    @abstractmethod
    def make_forecast_url(self):
        pass
