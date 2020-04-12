import cgi_parameters
from forecast_api import weather_api_forecast, static_api_forecast
from request_query_string_parser import RequestQueryStringParser

USE_API_ENDPOINT = False


def main():
    weather_api_query_string = cgi_parameters.get_cgi_url_query_string()
    query_parser = RequestQueryStringParser(weather_api_query_string)

    if not USE_API_ENDPOINT:
        query_parser.parsed_query_dict['format'] = 'json'
        api_forecast = static_api_forecast.StaticAPIForecast(query_parser)
    else:
        api_forecast = weather_api_forecast.WeatherAPIForecast(query_parser)

    print(api_forecast.make_content_type())
    print(api_forecast.fetch_and_map_response_as_string())


# Start application
main()
