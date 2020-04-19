import json
import datetime
import os
from abc import abstractmethod


def round_to_str(value: float):
    return str(round(value))


def unix_timestamp_to_world_weather_hourly_time(timestamp: float) -> str:
    time_int = int(datetime.datetime.fromtimestamp(timestamp).time().__format__("%H%M"))
    normalized_time_int = int(time_int / 300) * 300
    return str(normalized_time_int)


def unix_timestamp_to_world_weather_day_time(timestamp: float) -> str:
    return datetime.datetime.fromtimestamp(timestamp).time().__format__("%I:%M %p")


def make_resources_path():
    mapping_file_path = '../resources/'

    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, mapping_file_path)


class BaseForecastMapper:
    def __init__(self, json_string):
        self.forecast_input_dictionary = json.loads(json_string)

        self.corresponding_code_key = ''
        with open(make_resources_path() + 'condition-map.json', 'r') as conditions_map_json_file:
            self.conditions_mappings = json.loads(conditions_map_json_file.read())

    @abstractmethod
    def to_output_dictionary(self):
        pass

    def world_weather_code_by_corresponding_code(self, corresponding_code):
        return str(self.get_mapping_by_corresponding_code(corresponding_code)['code'])

    def get_mapping_by_corresponding_code(self, corresponding_code):
        if self.corresponding_code_key == '':
            raise NotImplementedError('corresponding code key not implemented for this class')

        for mapping in self.conditions_mappings:
            if self.corresponding_code_key in mapping['corresponding_codes']:
                codes_list = mapping['corresponding_codes'][self.corresponding_code_key]
                if corresponding_code in codes_list:
                    return mapping

        error_message = \
            'mapping not configured for key "{code_key}" and corresponding code "{code}"'.format(
                code_key=self.corresponding_code_key, code=corresponding_code
            )
        raise ValueError(error_message)

    def make_icon_url_by_corresponding_code(self, corresponding_code, is_day=True):
        day_symbol = 'day'
        if not is_day:
            day_symbol = 'night'

        mapping = self.get_mapping_by_corresponding_code(corresponding_code)
        return 'http://cdn.worldweatheronline.net/images/wsymbols01_png_64/{symbol}.png'\
            .format(symbol=mapping['symbol'][day_symbol])

    def get_condition_by_corresponding_code(self, corresponding_code):
        mapping = self.get_mapping_by_corresponding_code(corresponding_code)
        return mapping['description']['de']
