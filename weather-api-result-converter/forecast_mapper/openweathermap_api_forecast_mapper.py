from forecast_mapper.base_forecast_mapper import \
    BaseForecastMapper, \
    round_to_str, \
    unix_timestamp_to_world_weather_day_time
from forecast_mapper.weather_stats import degree_to_wind_rose_str


def merge_dicts(dict1, dict2):
    return {**dict1, **dict2}


class OpenweathermapAPIForecastMapper(BaseForecastMapper):

    def __init__(self, json_string):
        super().__init__(json_string)
        self.corresponding_code_key = 'openweathermap'

    def to_output_dictionary(self):
        source_dict = self.forecast_input_dictionary
        current = source_dict['current']
        temp_c = current['temp']

        return {
            'data': {
                'current_condition': [
                    merge_dicts({
                        # extra
                        'observation_time':
                            unix_timestamp_to_world_weather_day_time(current['dt']),
                        'temp_C': round_to_str(temp_c),
                        'visibility': round_to_str(current['visibility'] / 1000)
                    }, self.forecast_base_elements(current))
                ],
                'weather': self.to_weather_elements()
            }
        }

    def forecast_base_elements(self, forecast_element: dict):
        corresponding_code = forecast_element['weather'][0]['id']
        wind_direction = forecast_element['wind_deg']
        translated_wind_rose = self.translate_16_points_wind_direction(
            degree_to_wind_rose_str(wind_direction))
        return merge_dicts(self.parse_weather_by_corresponding_code(corresponding_code), {
            'windspeedKmph': round_to_str(forecast_element['wind_speed']),
            'winddirDegree': round_to_str(wind_direction),
            'winddir16Point': translated_wind_rose,
            'precipMM': self.parse_precipitation(forecast_element),
            'humidity': round_to_str(forecast_element['humidity']),
            'pressure': round_to_str(forecast_element['pressure']),
            'cloudcover': round_to_str(forecast_element['clouds'])
        })

    def parse_weather_by_corresponding_code(self, corresponding_code) -> dict:
        weather_code = self.world_weather_code_by_corresponding_code(corresponding_code)
        weather_icon = self.make_icon_url_by_corresponding_code(corresponding_code)
        weather_condition = self.get_condition_by_corresponding_code(corresponding_code)
        return {
            'weatherCode': str(weather_code),
            'weatherIconUrl': [{'value': weather_icon}],
            'weatherDesc': [{'value': weather_condition}]
        }

    @staticmethod
    def parse_precipitation(forecast_element):
        if 'rain' in forecast_element:
            precipitation = forecast_element['rain']
        else:
            precipitation = 0.0
        return str(precipitation)

    def to_weather_elements(self):
        source_dict = self.forecast_input_dictionary
        days = source_dict['daily']
        weather_elements = []
        for day_index in range(5):
            if len(days) > day_index:
                weather_elements.append(self.day_to_weather_element(days[day_index]))

        return weather_elements

    def day_to_weather_element(self, forecast_day: dict):
        return merge_dicts({
            'date': self.format_daily_date_by_locale_pattern(forecast_day['dt']),
            'windspeedKmph': str(forecast_day['wind_speed']),
            'precipMM': self.parse_precipitation(forecast_day),
            'tempMaxC': round_to_str(forecast_day['temp']['max']),
            'tempMinC': round_to_str(forecast_day['temp']['min']),
            'totalSnow_cm': self.parse_snow(forecast_day)
        }, self.parse_weather_by_corresponding_code(forecast_day['weather'][0]['id']))

    @staticmethod
    def parse_snow(forecast_element):
        if 'snow' in forecast_element:
            snow = forecast_element['snow'] / 10
        else:
            snow = 0.0
        return str(snow)
