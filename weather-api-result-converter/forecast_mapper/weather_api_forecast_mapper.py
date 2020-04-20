import datetime

from forecast_mapper.base_forecast_mapper import BaseForecastMapper, round_to_str


def weather_api_to_world_weather_code(weather_api_code: int):
    return str(weather_api_code - 887)


class WeatherAPIForecastMapper(BaseForecastMapper):

    def __init__(self, json_string):
        super().__init__(json_string)
        self.corresponding_code_key = 'weatherAPI'

    def to_output_dictionary(self):
        source_dict = self.forecast_input_dictionary
        current = source_dict['current']
        last_updated = datetime.datetime.fromtimestamp(current['last_updated_epoch'])
        corresponding_code = current['condition']['code']
        weather_code = self.world_weather_code_by_corresponding_code(corresponding_code)
        is_day = current['is_day'] != 0
        weather_icon = self.make_icon_url_by_corresponding_code(corresponding_code, is_day)
        weather_condition = self.get_condition_by_corresponding_code(corresponding_code)
        wind_dir = self.translate_16_points_wind_direction(current['wind_dir'])
        mapped = {
            'data': {
                'current_condition': [
                    {
                        'observation_time': last_updated.time().__format__("%I:%M %p"),
                        'temp_C': round_to_str(current['temp_c']),
                        'weatherCode': weather_code,
                        'weatherIconUrl': [{'value': weather_icon}],
                        'weatherDesc': [{'value': weather_condition}],
                        'windspeedKmph': round_to_str(current['wind_kph']),
                        'winddirDegree': round_to_str(current['wind_degree']),
                        'winddir16Point': wind_dir,
                        'precipMM': str(current['precip_mm']),
                        'humidity': round_to_str(current['humidity']),
                        'visibility': round_to_str(current['vis_km']),
                        'pressure': round_to_str(current['pressure_mb']),
                        'cloudcover': round_to_str(current['cloud'])
                    }
                ],
                'weather': self.to_weather_elements(wind_dir)
            }
        }

        return mapped

    def to_weather_elements(self, wind_dir):
        source_dict = self.forecast_input_dictionary
        weather_elements = []
        for forecast_day in source_dict['forecast']['forecastday']:
            weather_elements.append(self.forecast_day_to_weather_element(forecast_day, wind_dir))

        return weather_elements

    def forecast_day_to_weather_element(self, forecast_day: dict, wind_dir: str):
        day = forecast_day['day']

        corresponding_code = day['condition']['code']
        weather_code = self.world_weather_code_by_corresponding_code(corresponding_code)
        weather_icon = self.make_icon_url_by_corresponding_code(corresponding_code)
        weather_condition = self.get_condition_by_corresponding_code(corresponding_code)
        return {
            'date': self.format_daily_date_by_locale_pattern(forecast_day['date']),
            'weatherCode': weather_code,
            'weatherIconUrl': [{'value': weather_icon}],
            'weatherDesc': [{'value': weather_condition}],
            'tempMaxC': round_to_str(day['maxtemp_c']),
            'tempMinC': round_to_str(day['mintemp_c']),
            'windspeedKmph': str(day['maxwind_kph']),
            'precipMM': str(day['totalprecip_mm']),
            # not available in Weather-API, but maybe needed by MyGekko
            'totalSnow_cm': "0.0",
            # not provided with free api key
            'hourly': [{'time': '0', 'winddir16Point': wind_dir}],
        }
