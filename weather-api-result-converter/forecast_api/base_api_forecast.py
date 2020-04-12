import json
from abc import abstractmethod

from forecast_response_mapper import ForecastResponseMapper
from request_query_string_parser import RequestQueryStringParser


class BaseAPIForecast:
    def __init__(self, query_string_parser: RequestQueryStringParser):
        self.query_string_parser = query_string_parser

    def fetch_and_map_response_as_string(self):
        forecast_json = self.retrieve_json_from_endpoint()

        mapper = ForecastResponseMapper(forecast_json)
        mapped_dictionary = mapper.to_output_format()

        file_format = self.query_string_parser.retrieve_file_format()
        if file_format == 'json':
            return json.dumps(mapped_dictionary)

        if file_format == 'xml':
            raise NotImplementedError('xml output is not implemented')

        raise NotImplementedError('Unknown output format {format} not implemented'
                                  .format(format=file_format))

    @abstractmethod
    def retrieve_json_from_endpoint(self):
        pass
