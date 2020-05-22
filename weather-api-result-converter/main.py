import cgi_parameters
from forecast_api import openweathermap_api_forecast, weather_api_forecast
from request_query_string_parser import create_parser_with_default_values, RequestQueryStringParser

USE_STATIC_FILE = False


def main():
    if USE_STATIC_FILE:
        query_parser = create_parser_with_default_values()
    else:
        weather_api_query_string = cgi_parameters.get_cgi_url_query_string()
        query_parser = RequestQueryStringParser(weather_api_query_string)

    api_forecast = openweathermap_api_forecast\
        .OpenweathermapAPIForecast(query_parser, USE_STATIC_FILE)
#    api_forecast = weather_api_forecast.WeatherAPIForecast(query_parser, USE_STATIC_FILE)
    result = api_forecast.fetch_and_map_response_as_string()
    print(api_forecast.make_content_type())
    print(result)


# Start application
#import cgitb
#cgitb.enable(logdir="/var/log/weather-api-result-converter/")
main()
