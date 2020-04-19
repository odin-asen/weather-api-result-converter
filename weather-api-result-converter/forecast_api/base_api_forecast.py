import json
import dicttoxml
from abc import abstractmethod

from forecast_mapper.base_forecast_mapper import BaseForecastMapper
from request_query_string_parser import RequestQueryStringParser


class BaseAPIForecast:
    def __init__(self, query_string_parser: RequestQueryStringParser):
        self.query_string_parser = query_string_parser

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

    def make_content_type(self) -> str:
        return "Content-type: application/" + self.query_string_parser.retrieve_file_format()

    @abstractmethod
    def retrieve_json_string_from_endpoint(self) -> str:
        pass

    @abstractmethod
    def create_mapper(self, json_string: str) -> BaseForecastMapper:
        pass
