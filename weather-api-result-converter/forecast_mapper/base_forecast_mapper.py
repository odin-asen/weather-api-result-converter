import locale
import datetime
import json
import os
import os.path
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



DEFAULT_CONFIG = {
    'language_code': 'en',
    'locale': 'en_GB.UTF-8'
}


def load_mapping_config_or_default():
    if os.path.isfile('../config.json'):
        with open('../config.json', 'r') as config_json:
            return json.loads(config_json.read())
    else:
        return DEFAULT_CONFIG

class BaseForecastMapper:
    def __init__(self, json_string):
        self.forecast_input_dictionary = json.loads(json_string)
        mapping_config = load_mapping_config_or_default()
        self.language_code = mapping_config.get('language_code', DEFAULT_CONFIG['language_code'])
        self.locale = mapping_config.get('locale', DEFAULT_CONFIG['locale'])
        self.corresponding_code_key = ''
        with open(make_resources_path() + 'condition-map.json', 'r', encoding='utf-8') \
                as conditions_map_json_file:
            self.conditions_mappings = json.loads(conditions_map_json_file.read())

        translations_path = make_resources_path() + 'mapping-translations.json'
        with open(translations_path, 'r', encoding='utf-8') as translations_json_file:
            self.mapping_translations = json.loads(translations_json_file.read())

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

    def translate_16_points_wind_direction(self, short_code):
        return self.mapping_translations['wind_dir'][short_code][self.language_code]

    def get_condition_by_corresponding_code(self, corresponding_code):
        mapping = self.get_mapping_by_corresponding_code(corresponding_code)
        return mapping['description'][self.language_code]

    def format_daily_date_by_locale_pattern(self, timestamp: float) -> str:
        locale.setlocale(locale.LC_TIME, self.locale)
        date_pattern = self.mapping_translations['date_format']['day'][self.language_code]
        return datetime.datetime.fromtimestamp(timestamp).strftime(date_pattern)
