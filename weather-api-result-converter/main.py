import cgi_parameters
import static_api
import weather_api

USE_API_ENDPOINT = False


def main():
    if not USE_API_ENDPOINT:
        response_string = static_api.fetch_and_map_response_as_string()
    else:
        weather_api_path = cgi_parameters.get_cgi_url_path()
        weather_api_query_string = cgi_parameters.get_cgi_url_query_string()
        if not weather_api_path and not weather_api_query_string:
            response_string = \
                weather_api.fetch_and_map_response_as_string(
                    weather_api_path, weather_api_query_string)
        else:
            response_string = 'No path, no url parameters, no weather request!'

    print(response_string)


# Start application
main()
