import math


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


def windchill_celsius(temp: float, wind_speed_kph: float):
    if wind_speed_kph >= 5 and temp <= 10:
        return 13.12 + 0.6215 * temp + ((0.3965 * temp) - 11.37) * math.pow(wind_speed_kph, 0.16)

    return temp


def windchill_fahrenheit(temp: float, wind_speed_mph: float):
    if wind_speed_mph >= 3.125 and temp <= 50:
        return 35.74 + 0.6215 * temp + ((0.4275 * temp) - 35.75) * math.pow(wind_speed_mph, 0.16)

    return temp


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


def dew_point_celsius(temp: float, relative_humidity: float):
    temp_const_c = 257.14
    shift = 18.678
    gamma = log_n(relative_humidity / 100) + (shift * temp / (temp_const_c + temp))
    return temp_const_c * gamma / (shift - gamma)


def log_n(number: float):
    return math.log10(number) / math.log10(2.71828)


def dew_point_fahrenheit(temp: float, relative_humidity: float):
    if relative_humidity <= 50:
        return temp

    # approximation
    # https://en.wikipedia.org/wiki/Dew_point#Simple_approximation
    return temp - (0.36 * (100 - relative_humidity))
