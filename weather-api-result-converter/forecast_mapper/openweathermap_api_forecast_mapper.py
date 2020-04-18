import datetime
from statistics import mean

from forecast_mapper.base_forecast_mapper import \
    BaseForecastMapper, \
    round_to_str, \
    unix_timestamp_to_world_weather_day_time, \
    unix_timestamp_to_world_weather_hourly_time
from forecast_mapper.weather_stats import celsius_to_fahrenheit, kph_to_miles, mm_to_inch, h_pa_to_inches, \
    degree_to_wind_rose_str, heat_index_celsius, heat_index_fahrenheit, dew_point_celsius, \
    windchill_celsius


def forecast_main(dictionary: dict, key: str):
    return dictionary['main'][key]


def forecast_wind(dictionary: dict, key: str):
    return dictionary['wind'][key]


def total_snow_in_cm(forecast_list):
    elements_with_snow = filter(lambda el: 'snow' in el, forecast_list)
    return sum(map(lambda el: el['snow']['3h'], elements_with_snow)) / 10.0


def total_sunshine(forecast_list_for_one_day, sunrise: int, sunset: int):
    hour_interval = 3.0
    sunshine_hours = 0.0
    for forecast in forecast_list_for_one_day:
        time = forecast['dt']
        cloud_influence = 100 - forecast['clouds']['all']
        time_to_sunrise = sunrise - time
        time_to_sunset = sunset - time
        time_to_sunrise_in_hours = time_to_sunrise / 3600
        time_to_sunset_in_hours = time_to_sunset / 3600

        # it is full day
        if time_to_sunrise_in_hours <= 0.0 and time_to_sunset_in_hours >= hour_interval:
            sunshine_hours += hour_interval * cloud_influence / 100.0
        # it is partly day in the morning
        elif hour_interval > time_to_sunrise_in_hours > 0:
            sunshine_hours += (hour_interval - time_to_sunrise_in_hours) * cloud_influence / 100.0
        # it is partly day in the evening
        elif hour_interval > time_to_sunset_in_hours > 0:
            sunshine_hours += (hour_interval - time_to_sunset_in_hours) * cloud_influence / 100.0

    return sunshine_hours


def merge_dicts(dict1, dict2):
    return {**dict1, **dict2}


class OpenweathermapAPIForecastMapper(BaseForecastMapper):

    def __init__(self, json_string):
        super().__init__(json_string)
        self.corresponding_code_key = 'openweathermap'

    def to_output_dictionary(self):
        source_dict = self.forecast_input_dictionary
        current = source_dict['list'][0]
        current_timestamp = datetime.datetime.now().timestamp()
        temp_c = forecast_main(current, 'temp')

        return {
            'data': {
                'current_condition': [
                    # not yet provided with current implementation
                    # just taking the first element of list as current
                    merge_dicts(self.forecast_base_elements(current), {
                        # extra
                        'temp_C': round_to_str(temp_c),
                        'temp_F': round_to_str(celsius_to_fahrenheit(temp_c)),
                        'observation_time':
                            unix_timestamp_to_world_weather_day_time(current_timestamp),
                        # not provided
                        'uvIndex': 0
                    })
                ],
                'weather': self.to_weather_elements(),
                'ClimateAverages': [
                    # not provided
                ]
            }
        }

    def forecast_base_elements(self, forecast_element: dict):
        corresponding_code = forecast_element['weather'][0]['id']
        weather_code = self.world_weather_code_by_corresponding_code(corresponding_code)
        weather_icon = self.make_icon_url_by_corresponding_code(corresponding_code)
        weather_condition = self.get_condition_by_corresponding_code(corresponding_code)
        wind_speed = forecast_element['wind']['speed']
        wind_direction = forecast_element['wind']['deg']
        if 'rain' in forecast_element:
            precipitation_mm = forecast_element['rain']['3h']
        else:
            precipitation_mm = 0.0
        pressure_h_pa = forecast_main(forecast_element, 'grnd_level')
        temp_feelslike = forecast_main(forecast_element, 'feels_like')

        return {
            'windspeedKmph': round_to_str(wind_speed),
            'windspeedMiles': round_to_str(kph_to_miles(wind_speed)),
            'winddirDegree': round_to_str(wind_direction),
            'winddir16Point': degree_to_wind_rose_str(wind_direction),

            'weatherCode': weather_code,
            'weatherIconUrl': [{'value': weather_icon}],
            'weatherDesc': [{'value': weather_condition}],

            'precipMM': round_to_str(precipitation_mm),
            'precipInches': round_to_str(mm_to_inch(precipitation_mm)),
            'humidity': round_to_str(forecast_main(forecast_element, 'humidity')),

            # not provided
            'visibility': '0',
            # not provided
            'visibilityMiles': '0',

            'pressure': round_to_str(pressure_h_pa),
            'pressureInches': round_to_str(h_pa_to_inches(pressure_h_pa)),
            'cloudcover': round_to_str(forecast_element['clouds']['all']),
            'FeelsLikeC': round_to_str(temp_feelslike),
            'FeelsLikeF': round_to_str(celsius_to_fahrenheit(temp_feelslike)),
        }

    def to_weather_elements(self):
        source_dict = self.forecast_input_dictionary
        sunrise = source_dict['city']['sunrise']
        sunset = source_dict['city']['sunset']
        weather_elements = []
        # Group by day -> weather_element -> calc min, max, avg, cloudcover
        grouped_by_iso_day = {}
        for element in sorted(source_dict['list'], key=lambda el: el['dt']):
            group = datetime.datetime.fromtimestamp(element['dt']).__format__("%Y-%m-%d")
            grouped_by_iso_day.setdefault(group, []).append(element)

        # Build weather_element per day. hourly are the sub elements
        for iso_day, day_forecast_list in grouped_by_iso_day.items():
            day_temp_avg = mean(map(lambda el: forecast_main(el, 'temp'), day_forecast_list))
            day_temp_max = max(map(lambda el: forecast_main(el, 'temp_max'), day_forecast_list))
            day_temp_min = min(map(lambda el: forecast_main(el, 'temp_min'), day_forecast_list))

            weather_elements.append({
                'date': iso_day,
                # not provided
                'astronomy': [
                    {
                        'sunrise': '',
                        'sunset': '',
                        'moonrise': '',
                        'moonset': '',
                        'moon_phase': '',
                        'moon_illumination': '',
                    }
                ],
                'maxtempC': round_to_str(day_temp_max),
                'maxtempF': round_to_str(celsius_to_fahrenheit(day_temp_max)),
                'mintempC': round_to_str(day_temp_min),
                'mintempF': round_to_str(celsius_to_fahrenheit(day_temp_min)),
                'avgtempC': round_to_str(day_temp_avg),
                'avgtempF': round_to_str(celsius_to_fahrenheit(day_temp_avg)),
                'totalSnow_cm': str(total_snow_in_cm(day_forecast_list)),
                'sunHour': str(total_sunshine(day_forecast_list, sunrise, sunset)),
                # not provided
                'uvIndex': '0',
                'hourly': list(map(self.forecast_element_to_hourly_element, day_forecast_list))
            })

            # update sunrise and sunset for next day
            one_day_in_seconds = 24 * 60 * 60
            sunrise += one_day_in_seconds
            sunset += one_day_in_seconds

        return weather_elements

    def forecast_element_to_hourly_element(self, forecast_element: dict):
        temp = forecast_main(forecast_element, 'temp')
        temp_f = celsius_to_fahrenheit(temp)
        relative_humidity = forecast_main(forecast_element, 'humidity')
        dew_point = dew_point_celsius(temp, relative_humidity)
        wind_speed = forecast_element['wind']['speed']
        windchill = windchill_celsius(temp, wind_speed)

        return merge_dicts(self.forecast_base_elements(forecast_element), {
            # extra
            'tempC': round_to_str(temp),
            'tempF': round_to_str(celsius_to_fahrenheit(temp)),
            'time': unix_timestamp_to_world_weather_hourly_time(forecast_element['dt']),
            'HeatIndexC': round_to_str(heat_index_celsius(temp, relative_humidity)),
            'HeatIndexF': round_to_str(heat_index_fahrenheit(temp_f, relative_humidity)),
            'DewPointC': round_to_str(dew_point),
            'DewPointF': round_to_str(celsius_to_fahrenheit(dew_point)),
            'WindChillC': round_to_str(windchill),
            'WindChillF': round_to_str(celsius_to_fahrenheit(windchill))
        })
