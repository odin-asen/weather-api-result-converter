import datetime

from forecast_mapper.base_forecast_mapper import BaseForecastMapper, round_to_str


def weather_api_to_world_weather_code(weather_api_code: int):
    return str(weather_api_code - 887)


def forecast_day_to_weather_element(forecast_day: dict):
    day = forecast_day['day']
    astro = forecast_day['astro']

    # Could not test this part, because no premium API Key available for weatherapi.com
    hourly_elements = []
    if 'hour' in forecast_day:
        for forecast_day_hour in forecast_day['hour']:
            hourly_elements.append(forecast_day_hour_to_hourly_element(forecast_day_hour))

    return {
        'date': forecast_day['date'],
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


def forecast_day_hour_to_hourly_element(forecast_day_hour: dict):
    time_epoch = datetime.datetime.fromtimestamp(forecast_day_hour['time_epoch'])

    return {
        'time': str(int(time_epoch.time().__format__("%I%M"))),
        'tempC': round_to_str(forecast_day_hour['temp_c']),
        'tempF': round_to_str(forecast_day_hour['temp_f']),
        'windspeedMiles': round_to_str(forecast_day_hour['wind_mph']),
        'windspeedKmph': round_to_str(forecast_day_hour['wind_kph']),
        'winddirDegree': round_to_str(forecast_day_hour['wind_degree']),
        'winddir16Point': forecast_day_hour['wind_dir'],
        'weatherCode':
            weather_api_to_world_weather_code(forecast_day_hour['condition']['code']),
        'weatherIconUrl': [
            {
                'value': 'http:' + forecast_day_hour['condition']['icon']
            }
        ],
        'weatherDesc': [
            {
                'value': forecast_day_hour['condition']['text']
            }
        ],
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


class OpenweathermapAPIForecastMapper(BaseForecastMapper):

    def to_output_dictionary(self):
        source_dict = self.forecast_input_dictionary
        current = source_dict['current']
        last_updated = datetime.datetime.fromtimestamp(current['last_updated_epoch'])
        mapped = {
            'data': {
                'current_condition': [
                    {
                        'observation_time': last_updated.time().__format__("%I:%M %p"),
                        'temp_C': round_to_str(current['temp_c']),
                        'temp_F': round_to_str(current['temp_f']),
                        'weatherCode':
                            weather_api_to_world_weather_code(current['condition']['code']),
                        'weatherIconUrl': [
                            {
                                'value': 'http:' + current['condition']['icon']
                            }
                        ],
                        'weatherDesc': [
                            {
                                'value': current['condition']['text']
                            }
                        ],
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
                        'cloudcover': round_to_str(current['cloud']),
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
            weather_elements.append(forecast_day_to_weather_element(forecast_day))

        return weather_elements
