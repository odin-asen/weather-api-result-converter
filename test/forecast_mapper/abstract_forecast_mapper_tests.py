import json
from abc import abstractmethod
from unittest import TestCase

from forecast_mapper.base_forecast_mapper import BaseForecastMapper
from test.forecast_mapper.forecast_mapper_test_suite import read_output_test_json


# noinspection Pylint
class AbstractForecastMapperTest():
    @abstractmethod
    def prepare_test_object(self) -> BaseForecastMapper:
        pass

    @abstractmethod
    def expected_output_file_name(self) -> str:
        pass

    def GIVEN_api_test_json_WHEN_to_output_dictionary_THEN_map_json_to_expected_json(self, test_case: TestCase):
        test_object = self.prepare_test_object()
        expected_output_dict = json.loads(read_output_test_json(self.expected_output_file_name()))

        mapped_dict = test_object.to_output_dictionary()

        test_case.assertEqual(expected_output_dict, mapped_dict)

    def GIVEN_translation_to_de_WHEN_to_output_dictionary_THEN_decode_umlaut_as_expected(self, test_case: TestCase):
        test_object = self.prepare_test_object()
        test_object.language_code = 'de'

        mapped_dict = test_object.to_output_dictionary()

        test_case.assertEqual('Leicht bewolkt', mapped_dict['data']['weather'][0]['weatherDesc'][0]['value'])

    def GIVEN_translation_to_de_WHEN_to_output_dictionary_THEN_print_date_in_German(self, test_case: TestCase):
        test_object = self.prepare_test_object()
        test_object.language_code = 'de'

        mapped_dict = test_object.to_output_dictionary()

        test_case.assertEqual('08. April', mapped_dict['data']['weather'][0]['date'])

    def GIVEN_translation_to_en_WHEN_to_output_dictionary_THEN_print_date_in_English(self, test_case: TestCase):
        test_object = self.prepare_test_object()
        test_object.language_code = 'en'

        mapped_dict = test_object.to_output_dictionary()

        test_case.assertEqual('April 08', mapped_dict['data']['weather'][0]['date'])
