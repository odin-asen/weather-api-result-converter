import json
from abc import abstractmethod


def round_to_str(value: float):
    return str(round(value))


# noinspection Pylint
class BaseForecastMapper:
    def __init__(self, json_string):
        self.forecast_input_dictionary = json.loads(json_string)

    @abstractmethod
    def to_output_dictionary(self):
        pass
