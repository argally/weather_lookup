"""
Openweather API module

This module will take a value for latitude and longitude 
and request Weather data for these coordinates from Openweather API

A value of current temperature in Celsius is returned
"""

import json
import sys

import requests

# Global to reference the base URL to use for queries to Openweather API
BASE_URL = "https://api.openweathermap.org/data/2.5/onecall"


def get_temp(lat, lon, api_key):
    """
    Construct the full API URL which will use
    latitude and longitude to retrieve weather data.
    Unit of measurement should be Celsius i.e units=metric
    Include following parameters
    :param lat:
    :param lon:
    :param api_key:
    """
    try:
        url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code != 200:
            response = "N/A"
            return response
        else:
            weather_data = response.json()
            return weather_data["current"]["temp"]
    except requests.exceptions.RequestException as error:
        sys.exit(1)
