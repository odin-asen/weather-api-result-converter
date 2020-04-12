import requests
import json

#apiKey = "43be7304c7404523b79191056200604"
#location="Singen"
#jsonResponse = requests.get("http://api.weatherapi.com/v1/forecast.json?key=" + apiKey + "&q=" + location + "&days=5")
#print(jsonResponse.text)
#print(jsonResponse.json()['location'])

# def as_forecastResult(dictionary):
#     res = ForecastResult()
#     res.__dict__.update(dictionary)


#json.loads(jsonResponse.text, object_hook=as_forecastResult)

def fetch_and_map_response_as_string(weather_api_path, weather_api_query_string):
    return ''
