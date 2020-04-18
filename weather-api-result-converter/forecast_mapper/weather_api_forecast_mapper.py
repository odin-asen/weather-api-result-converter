import datetime

from forecast_mapper.base_forecast_mapper import BaseForecastMapper, round_to_str, \
    unix_timestamp_to_world_weather_hourly_time


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
        weather_icon = self.make_icon_url_by_corresponding_code(corresponding_code)
        weather_condition = self.get_condition_by_corresponding_code(corresponding_code)
        mapped = {
            'data': {
                'current_condition': [
                    {
                        'observation_time': last_updated.time().__format__("%I:%M %p"),
                        'temp_C': round_to_str(current['temp_c']),
                        'temp_F': round_to_str(current['temp_f']),
                        'weatherCode': weather_code,
                        'weatherIconUrl': [{'value': weather_icon}],
                        'weatherDesc': [{'value': weather_condition}],
                        'windspeedMiles': round_to_str(current['wind_mph']),
                        'windspeedKmph': round_to_str(current['wind_kph']),
                        'winddirDegree': round_to_str(current['wind_degree']),
                        'winddir16Point': current['wind_dir'],
                        'precipMM': str(current['precip_mm']),
                        'precipInches': str(current['precip_in']),
                        'humidity': round_to_str(current['humidity']),
                        'visibility': round_to_str(current['vis_km']),
                        'visibilityMiles': round_to_str(current['vis_miles']),
                        'pressure': round_to_str(current['pressure_mb']),
                        'pressureInches': round_to_str(current['pressure_in']),
                        'cloud_cover': round_to_str(current['cloud']),
                        'cloudCover': round_to_str(current['cloud']),
                        'FeelsLikeC': round_to_str(current['feelslike_c']),
                        'FeelsLikeF': round_to_str(current['feelslike_f']),
                        'uvIndex': round(current['uv'])
                    }
                ],
                'weather': self.to_weather_elements(),
                'ClimateAverages': [
                    # does not exist on Weather-API
                ]
            }
        }

        return mapped

    def to_weather_elements(self):
        source_dict = self.forecast_input_dictionary
        weather_elements = []
        for forecast_day in source_dict['forecast']['forecastday']:
            weather_elements.append(self.forecast_day_to_weather_element(forecast_day))

        return weather_elements

    def forecast_day_to_weather_element(self, forecast_day: dict):
        day = forecast_day['day']
        astro = forecast_day['astro']

        # Could not test this part, because no premium API Key available for weatherapi.com
        hourly_elements = []
        if 'hour' in forecast_day:
            for forecast_day_hour in forecast_day['hour']:
                hourly_elements.append(self.forecast_day_hour_to_hourly_element(forecast_day_hour))

        date_array = forecast_day['date'].split("-")
        return {
            'date': date_array[2] + '.' + date_array[1] + '.' + date_array[0],
            'weatherCode': '308',
            'astronomy': [
                {
                    'sunrise': astro.get('sunrise', ''),
                    'sunset': astro.get('sunset', ''),
                    'moonrise': astro.get('moonrise', ''),
                    'moonset': astro.get('moonset', ''),
                    'moon_phase': astro.get('moon_phase', ''),
                    'moon_illumination': astro.get('moon_illumination', '')
                }
            ],
            'maxtempC': round_to_str(day['maxtemp_c']),
            'maxtempF': round_to_str(day['maxtemp_f']),
            'mintempC': round_to_str(day['mintemp_c']),
            'mintempF': round_to_str(day['mintemp_f']),
            'avgtempC': round_to_str(day['avgtemp_c']),
            'avgtempF': round_to_str(day['avgtemp_f']),
            # not available in Weather-API
            'totalSnow_cm': "0.0",
            # not available in Weather-API
            'sunHour': "0.0",
            'uvIndex': round_to_str(day['uv']),
            'hourly': hourly_elements
        }

    def forecast_day_hour_to_hourly_element(self, forecast_day_hour: dict):
        corresponding_code = forecast_day_hour['condition']['code']
        weather_code = self.world_weather_code_by_corresponding_code(corresponding_code)
        weather_icon = self.make_icon_url_by_corresponding_code(corresponding_code)
        weather_condition = self.get_condition_by_corresponding_code(corresponding_code)
        return {
            'time': unix_timestamp_to_world_weather_hourly_time(forecast_day_hour['time_epoch']),
            'tempC': round_to_str(forecast_day_hour['temp_c']),
            'tempF': round_to_str(forecast_day_hour['temp_f']),
            'windspeedMiles': round_to_str(forecast_day_hour['wind_mph']),
            'windspeedKmph': round_to_str(forecast_day_hour['wind_kph']),
            'winddirDegree': round_to_str(forecast_day_hour['wind_degree']),
            'winddir16Point': forecast_day_hour['wind_dir'],
            'weatherCode': weather_code,
            'weatherIconUrl': [{'value': weather_icon}],
            'weatherDesc': [{'value': weather_condition}],
            'precipMM': str(forecast_day_hour['precip_mm']),
            'precipInches': str(forecast_day_hour['precip_in']),
            'humidity': round_to_str(forecast_day_hour['humidity']),
            'visibility': round_to_str(forecast_day_hour['vis_km']),
            'visibilityMiles': round_to_str(forecast_day_hour['vis_miles']),
            'pressure': round_to_str(forecast_day_hour['pressure_mb']),
            'pressureInches': round_to_str(forecast_day_hour['pressure_in']),
            'cloudcover': round_to_str(forecast_day_hour['cloud']),
            'HeatIndexC': round_to_str(forecast_day_hour['heatindex_c']),
            'HeatIndexF': round_to_str(forecast_day_hour['heatindex_f']),
            'DewPointC': round_to_str(forecast_day_hour['dewpoint_c']),
            'DewPointF': round_to_str(forecast_day_hour['dewpoint_f']),
            'WindChillC': round_to_str(forecast_day_hour['windchill_c']),
            'WindChillF': round_to_str(forecast_day_hour['windchill_f']),
            'WindGustMiles': round_to_str(forecast_day_hour['gust_mph']),
            'WindGustKmph': round_to_str(forecast_day_hour['gust_kph']),
            'FeelsLikeC': round_to_str(forecast_day_hour['feelslike_c']),
            'FeelsLikeF': round_to_str(forecast_day_hour['feelslike_f']),
            'chanceofrain': round_to_str(forecast_day_hour['chance_of_rain']),
            'chanceofsnow': round_to_str(forecast_day_hour['chance_of_snow'])
        }
