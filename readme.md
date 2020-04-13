# About
Access a weather API forecast endpoint over HTTP and convert it to another format.

## Python version
* Python 3.7

## Supported API
* `api.weatherapi.com`

# Usage
Copy the folder `weather-api-result-converter` somewhere to your system and execute `main.py`.
The script prints the converted result as JSON to the stream output.
For example, if you use the script with CGI, CGI will receive the JSON as response and will process the response
accordingly.

## With CGI in lighttpd webserver
The project contains a [minimum configuration](lighttpd/minimum.conf) for lighttpd to include into the webserver.

On Linux, you can copy the [source folder](weather-api-result-converter) to `/opt/` and make the main.py script
executable with `chmod +x /opt/weather-api-result-converter/main.py`

Then, include the minimum configuration example to your lighttpd webserver and modify it to fit to your requirements.

## Development
To test modifications the resources folder contains static files which can be used to test the data mapping to the
desired response schema.

## Installation (dependencies)
Apart from builtin modules, this application requires third-party python packages
* [dicttoxml](https://pypi.org/project/dicttoxml/), at least version 1.7.4

Before calling `main.py` you need to install these dependencies with pip, e.g. `pip install dicttoxml` or 
`pip3 install dicttoxml`.
 