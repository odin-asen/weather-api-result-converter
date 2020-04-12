import datetime


def weather_api_to_world_weather_code(weather_api_code: int):
    return str(weather_api_code - 887)


def round_to_str(value: float):
    return str(round(value))


def forecast_day_to_weather_element(forecast_day: dict):
    day = forecast_day['day']
    astro = forecast_day['astro']
    weather_element = {
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
        'hourly': [
            # not available in Weather-API
        ]
    }
    return weather_element


class ForecastResponseMapper:
    def __init__(self, forecast_response_dictionary):
        self.response_dictionary = forecast_response_dictionary

    def to_world_weather_online_format(self):
        source_dict = self.response_dictionary
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
        source_dict = self.response_dictionary
        weather_elements = []
        for forecast_day in source_dict['forecast']['forecastday']:
            weather_elements.append(forecast_day_to_weather_element(forecast_day))

        return weather_elements
