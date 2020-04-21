from unittest import TestCase

from forecast_mapper.base_forecast_mapper import BaseForecastMapper
from forecast_mapper.openweathermap_api_forecast_mapper import OpenweathermapAPIForecastMapper
from test.forecast_mapper.abstract_forecast_mapper_tests import AbstractForecastMapperTest
from test.forecast_mapper.forecast_mapper_test_suite import read_input_test_json


# noinspection Pylint
class TestWeatherAPIForecastMapper(AbstractForecastMapperTest, TestCase):
    def prepare_test_object(self) -> BaseForecastMapper:
        test_json = read_input_test_json('openweathermap-api-forecast')
        return OpenweathermapAPIForecastMapper(test_json)

    def expected_output_file_name(self) -> str:
        return 'expected-openweathermap-output-for-mygekko'

    def test_base_mapper_functions(self):
        self.GIVEN_api_test_json_WHEN_to_output_dictionary_THEN_map_json_to_expected_json(self)
        self.GIVEN_translation_to_de_WHEN_to_output_dictionary_THEN_decode_umlaut_as_expected(self)
        self.GIVEN_translation_to_de_WHEN_to_output_dictionary_THEN_print_date_in_German(self)
        self.GIVEN_translation_to_en_WHEN_to_output_dictionary_THEN_print_date_in_English(self)
