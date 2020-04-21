from unittest import TestCase
import json

from forecast_mapper.weather_api_forecast_mapper import WeatherAPIForecastMapper
from test.forecast_mapper.forecast_mapper_test_suite import read_output_test_json, read_input_test_json


def prepare_test_object() -> WeatherAPIForecastMapper:
    test_json = read_input_test_json('weather-api-forecast')
    return WeatherAPIForecastMapper(test_json)


# noinspection Pylint
class TestWeatherAPIForecastMapper(TestCase):
    def test_GIVEN_weather_api_test_json_WHEN_to_output_dictionary_THEN_map_json_to_expected_json(self):
        test_object = prepare_test_object()
        expected_output_dict = json.loads(read_output_test_json('expected-output-for-mygekko'))

        mapped_dict = test_object.to_output_dictionary()

        self.assertEqual(expected_output_dict, mapped_dict)

    def test_GIVEN_translation_to_de_WHEN_to_output_dictionary_THEN_decode_umlaut_as_expected(self):
        test_object = prepare_test_object()
        test_object.language_code = 'de'

        mapped_dict = test_object.to_output_dictionary()

        self.assertEqual('Leicht bewolkt', mapped_dict['data']['weather'][0]['weatherDesc'][0]['value'])

    def test_GIVEN_translation_to_de_WHEN_to_output_dictionary_THEN_print_date_in_German(self):
        test_object = prepare_test_object()
        test_object.language_code = 'de'

        mapped_dict = test_object.to_output_dictionary()

        self.assertEqual('08. April', mapped_dict['data']['weather'][0]['date'])

    def test_GIVEN_translation_to_en_WHEN_to_output_dictionary_THEN_print_date_in_German(self):
        test_object = prepare_test_object()
        test_object.language_code = 'en'

        mapped_dict = test_object.to_output_dictionary()

        self.assertEqual('April 08', mapped_dict['data']['weather'][0]['date'])
