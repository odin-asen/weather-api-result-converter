import cgitb
import cgi_parameters
from forecast_api import weather_api_forecast
from request_query_string_parser import RequestQueryStringParser

USE_STATIC_FILE = True


def main():
    weather_api_query_string = cgi_parameters.get_cgi_url_query_string()
    query_parser = RequestQueryStringParser(weather_api_query_string)

    if USE_STATIC_FILE:
        query_parser.parsed_query_dict['format'] = 'json'

    api_forecast = weather_api_forecast.WeatherAPIForecast(query_parser, USE_STATIC_FILE)
    print(api_forecast.fetch_and_map_response_as_string())


# Start application
cgitb.enable(logdir="/var/log/weather-api-result-converter/")
main()
