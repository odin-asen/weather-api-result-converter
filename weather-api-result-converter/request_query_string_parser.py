from urllib.parse import parse_qs


class RequestQueryStringParser:
    def __init__(self, request_query_string: str):
        self.parsed_query_dict = parse_qs(request_query_string)

    def has_api_key(self):
        return 'key' in self.parsed_query_dict

    def retrieve_api_key(self):
        return self.parsed_query_dict['key']

    def has_search_query(self):
        return 'q' in self.parsed_query_dict

    def retrieve_search_query(self):
        return self.parsed_query_dict['q']

    def retrieve_file_format(self):
        if 'format' in self.parsed_query_dict:
            return self.parsed_query_dict['format']

        return 'xml'

    def retrieve_requested_days(self):
        if 'num_of_days' in self.parsed_query_dict:
            return self.parsed_query_dict['num_of_days']

        return 5
