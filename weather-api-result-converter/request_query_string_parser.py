from urllib.parse import parse_qs


class RequestQueryStringParser:
    def __init__(self, request_query_string: str):
        self.parsed_query_dict = parse_qs(request_query_string)

    def has_api_key(self):
        return 'key' in self.parsed_query_dict

    def retrieve_api_key(self):
        return self.parsed_query_dict['key'][0]

    def has_search_query(self):
        return 'q' in self.parsed_query_dict

    def retrieve_search_query(self):
        return self.parsed_query_dict['q'][0]

    def retrieve_file_format(self, default_value='xml'):
        return self.retrieve_value_or_default('format', default_value)

    def retrieve_requested_days(self, default_value=5):
        return int(self.retrieve_value_or_default('num_of_days', default_value))

    def retrieve_value_or_default(self, value_name, default_value):
        if value_name in self.parsed_query_dict:
            return self.parsed_query_dict[value_name][0]

        return default_value


def create_parser_with_default_values() -> RequestQueryStringParser:
    return RequestQueryStringParser('key=&q=&format=json')
