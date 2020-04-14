import datetime

from forecast_mapper.base_forecast_mapper import \
    BaseForecastMapper, \
    round_to_str, \
    unix_timestamp_to_world_weather_day_time


def celsius_to_fahrenheit(celsius: float):
    return celsius * 1.8 + 32


def kph_to_miles(kph: float):
    return kph * 1.6


def mm_to_inch(milli_meter: float):
    return milli_meter / 2.54


def h_pa_to_inches(h_pa: float):
    return h_pa * 0.0295299830714447


def degree_to_wind_rose_str(degree: float):
    values = [
        'N', 'NNE', 'NE', 'ENE',
        'E', 'ESE', 'SE', 'SSE',
        'S', 'SSW', 'SW', 'WSW',
        'W', 'WNW', 'NW', 'NNW'
    ]
    circle_span = 360.0
    segment_span = circle_span / len(values)

    half_segment_span = segment_span / 2
    degree_integer_ratio = int(degree / circle_span)
    normalized_degree = half_segment_span + degree - degree_integer_ratio * circle_span

    segment_number = int(normalized_degree / segment_span)
    if segment_number == len(values):
        segment_number = 0

    return values[segment_number]


def forecast_day_to_weather_element(forecast_day: dict):
    day = forecast_day['day']
    astro = forecast_day['astro']

    # Could not test this part, because no premium API Key available for weatherapi.com
    hourly_elements = []
    #    if 'hour' in forecast_day:
    #        for forecast_day_hour in forecast_day['hour']:
    #            hourly_elements.append(forecast_day_hour_to_hourly_element(forecast_day_hour))

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


class OpenweathermapAPIForecastMapper(BaseForecastMapper):

    def __init__(self, json_string):
        super().__init__(json_string)
        self.corresponding_code_key = 'openweathermap'

    def to_output_dictionary(self):
        source_dict = self.forecast_input_dictionary
        current = source_dict['list'][0]
        current_timestamp = datetime.datetime.now().timestamp()

        current_corresponding_code = current['weather'][0]['id']
        return {
            'data': {
                'current_condition': [
                    # not yet provided with current implementation
                    # just taking the first element of list as current
                    {
                        'observation_time':
                            unix_timestamp_to_world_weather_day_time(current_timestamp),
                        'temp_C': round_to_str(current['main']['temp']),
                        'temp_F': round_to_str(celsius_to_fahrenheit(current['main']['temp'])),
                        'weatherCode':
                            self.world_weather_code_by_corresponding_code(
                                current_corresponding_code),
                        'weatherIconUrl':
                            [
                                {
                                    'value': self.make_icon_url_by_corresponding_code(
                                        current_corresponding_code)
                                }
                            ],
                        'weatherDesc':
                            [
                                {
                                    'value': self.get_condition_by_corresponding_code(
                                        current_corresponding_code)
                                }
                            ],
                        'windspeedMiles': round_to_str(
                            kph_to_miles(current['wind']['speed'])),
                        'windspeedKmph': round_to_str(current['wind']['speed']),
                        'winddirDegree': round_to_str(current['wind']['deg']),
                        'winddir16Point': degree_to_wind_rose_str(current['wind']['deg']),
                        'precipMM': round_to_str(current['rain']['3h']),
                        'precipInches': round_to_str(mm_to_inch(current['rain']['3h'])),
                        'humidity': round_to_str(current['main']['humidity']),
                        # not available
                        'visibility': '0',
                        # not available
                        'visibilityMiles': '',
                        'pressure': round_to_str(current['main']['grnd_level']),
                        'pressureInches': round_to_str(
                            h_pa_to_inches(current['main']['grnd_level'])),
                        'cloudcover': round_to_str(current['clouds']['all']),
                        'FeelsLikeC': round_to_str(current['main']['feels_like']),
                        'FeelsLikeF': round_to_str(
                            celsius_to_fahrenheit(current['main']['feels_like'])),
                        # not available
                        'uvIndex': 0
                    }
                ],
                # TODO implement weather elements
                'weather': self.to_weather_elements(),
                'ClimateAverages': [
                    # does not exist on Weather-API
                ]
            }
        }

    def to_weather_elements(self):
        source_dict = self.forecast_input_dictionary
        weather_elements = []
        for forecast_day in source_dict['forecast']['forecastday']:
            weather_elements.append(forecast_day_to_weather_element(forecast_day))

        return weather_elements

    def forecast_day_hour_to_hourly_element(self, forecast_day_hour: dict):
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
                self.world_weather_code_by_corresponding_code(forecast_day_hour['weather']['id']),
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
