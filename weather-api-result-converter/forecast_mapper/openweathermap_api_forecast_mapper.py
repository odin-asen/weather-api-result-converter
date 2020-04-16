import datetime
import math
from statistics import mean

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


def heat_index_celsius(temp: float, relative_humidity: float):
    if temp < 26.5:
        return temp

    return heat_index([-8.784695, 1.61139411, 2.338549,
                       -0.14611605, -0.012308094, -0.016424828,
                       0.002211732, 0.00072546, -0.000003582],
                      temp, relative_humidity)


def heat_index_fahrenheit(temp: float, relative_humidity: float):
    if temp < 79.5:
        return temp

    return heat_index([-42.379, 2.04901523, 10.1433127,
                       -0.22475541, -0.00683783, -0.05481717,
                       0.00122874, 0.00085282, -0.00000199],
                      temp, relative_humidity)


def heat_index(temp_consts: list, temp: float, relative_humidity: float):
    temp_square = temp * temp
    humidity_square = relative_humidity * relative_humidity
    return temp_consts[0] + temp_consts[1] * temp + temp_consts[2] * relative_humidity + \
           temp_consts[3] * temp * relative_humidity + temp_consts[4] * temp_square + \
           temp_consts[5] * humidity_square + temp_consts[6] * temp_square * relative_humidity + \
           temp_consts[7] * temp * humidity_square + temp_consts[8] * temp_square * humidity_square


def log_n(number: float):
    return math.log10(number) / math.log10(2.71828)


def dew_point_celsius(temp: float, relative_humidity: float):
    temp_const_c = 257.14
    shift = 18.678
    gamma = log_n(relative_humidity / 100) + (shift * temp / (temp_const_c + temp))
    return temp_const_c * gamma / (shift - gamma)


def dew_point_fahrenheit(temp: float, relative_humidity: float):
    if relative_humidity <= 50:
        return temp

    # approximation
    # https://en.wikipedia.org/wiki/Dew_point#Simple_approximation
    return temp - (0.36 * (100 - relative_humidity))


def forecast_main(dictionary: dict, key: str):
    return dictionary['main'][key]


def forecast_wind(dictionary: dict, key: str):
    return dictionary['wind'][key]


def total_snow_in_cm(forecast_list):
    elements_with_snow = filter(lambda el: 'snow' in el, forecast_list)
    return sum(map(lambda el: el['snow']['3h'], elements_with_snow)) / 10.0


def total_sunshine(forecast_list):
    day_hours = 3.0 * len(forecast_list)
    # include sunset and sunrise,
    # calculate time to sunset, return partial value
    # after sunset, return 0
    # before sunrise, return 0
    # calculate time until sunrise, return partial value
    avg_sunshine = mean(map(lambda el: el['clouds']['all'], forecast_list))
    no_sunshine = day_hours * avg_sunshine / 100.0
    return day_hours - no_sunshine


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

        return {
            'data': {
                'current_condition': [
                    # not yet provided with current implementation
                    # just taking the first element of list as current
                    merge_dicts(self.forecast_base_elements(current), {
                        # extra
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
        temp_c = forecast_main(forecast_element, 'temp')
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
            'temp_C': round_to_str(temp_c),
            'temp_F': round_to_str(celsius_to_fahrenheit(temp_c)),

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
                'sunHour': str(total_sunshine(day_forecast_list)),
                # not provided
                'uvIndex': '0',
                'hourly': list(map(self.forecast_element_to_hourly_element, day_forecast_list))
            })

        return weather_elements

    def forecast_element_to_hourly_element(self, forecast_element: dict):
        time_epoch = datetime.datetime.fromtimestamp(forecast_element['dt'])
        temp = forecast_main(forecast_element, 'temp')
        temp_f = celsius_to_fahrenheit(temp)
        relative_humidity = forecast_main(forecast_element, 'humidity')
        dew_point = dew_point_celsius(temp, relative_humidity)

        return merge_dicts(self.forecast_base_elements(forecast_element), {
            # extra
            'time': str(int(time_epoch.time().__format__("%I%M"))),
            'HeatIndexC': round_to_str(heat_index_celsius(temp, relative_humidity)),
            'HeatIndexF': round_to_str(heat_index_fahrenheit(temp_f, relative_humidity)),
            'DewPointC': round_to_str(dew_point),
            'DewPointF': round_to_str(celsius_to_fahrenheit(dew_point))
            # 'WindChillC': round_to_str(forecast_element['windchill_c']),
            # 'WindChillF': round_to_str(forecast_element['windchill_f']),
            # 'WindGustMiles': round_to_str(forecast_element['gust_mph']),
            # 'WindGustKmph': round_to_str(forecast_element['gust_kph']),
            # 'chanceofrain': round_to_str(forecast_element['chance_of_rain']),
            # 'chanceofsnow': round_to_str(forecast_element['chance_of_snow'])
        })
