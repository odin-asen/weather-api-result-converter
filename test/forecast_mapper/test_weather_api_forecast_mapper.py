from unittest import TestCase

from forecast_mapper.weather_api_forecast_mapper import WeatherAPIForecastMapper
import json


RESOURCES_BASE = '../resources/json/'


def read_input_test_json() -> str:
    file_path = '{base}in/weather-api-forecast.json'.format(base=RESOURCES_BASE)
    with open(file_path, 'r') as json_file:
        return json_file.read()


def read_output_test_json() -> str:
    file_path = '{base}out/expected-output-for-mygekko.json'.format(base=RESOURCES_BASE)
    with open(file_path, 'r') as json_file:
        return json_file.read()


# noinspection Pylint
class TestWeatherAPIForecastMapper(TestCase):

    def test_GIVEN_weather_api_test_json_WHEN_to_output_dictionary_THEN_map_json_to_expected_json(self):
        test_json = read_input_test_json()
        expected_output_json = read_output_test_json()
        expected_output_dict = json.loads(expected_output_json)

        mapper = WeatherAPIForecastMapper(test_json)
        mapped_dict = mapper.to_output_dictionary()

        self.assertEqual(expected_output_dict, mapped_dict)

    def test_GIVEN_translation_to_de_WHEN_to_output_dictionary_THEN_decode_umlaut_as_expected(self):
        test_json = read_input_test_json()
        expected_output_json = read_output_test_json()
        expected_output_dict = json.loads(expected_output_json)

        mapper = WeatherAPIForecastMapper(test_json)
        mapper.language_code = 'de'
        mapped_dict = mapper.to_output_dictionary()

        self.assertEqual('Leicht bewölkt', mapped_dict['data']['weather'][0]['weatherDesc'][0]['value'])
