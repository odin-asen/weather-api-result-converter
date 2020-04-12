import json
from forecast_response_mapper import ForecastResponseMapper

STATIC_FILES_ROOT = 'resources/weather-api/'


def fetch_and_map_response_as_string():
    with open(STATIC_FILES_ROOT + 'forecast-singen.json', 'r') as forecast_json_file:
        forecast_json_string = forecast_json_file.read()
        forecast_json = json.loads(forecast_json_string)

    mapper = ForecastResponseMapper(forecast_json)
    mapped_dictionary = mapper.to_world_weather_online_format()

    return json.dumps(mapped_dictionary)
