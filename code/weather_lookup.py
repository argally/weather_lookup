"""
OpenWeather API using Apache access log

Parse unstructured Apache access logs and return filtered Host IPs based on following criteria:

Log entry occurred between Monday - Friday only
Log entry contains one of the following HTTP status codes 500, 502, 503, 504, 505

Take list of Host IP addresses using MaxMinds GeoLite2-City database
perform a Country lookup of each Host IP address and retrieve corresponding
location data.

For the 3 countries with the highest matched linecount perform a weather lookup
using the Openweathermap API and location data to ascertain the current temperature
for the given country (https://openweathermap.org/current)
"""

from argparse import ArgumentParser
import itertools

from geoip_lookup import geoip_lookup, top_three_location
from log_normalize import normalized_result
from openweather import get_temp


def main():
    """
    Command-line interface to request access log name
    and API key for Openweather API
    """
    parser = ArgumentParser(description="Retrieve access log and API key")
    parser.add_argument("log_file", action="store")
    parser.add_argument("api_key", action="store")
    args = parser.parse_args()
    
    with open(args.log_file, "r") as reader:
        log_entries = reader.readlines()
    parsed = normalized_result(log_entries)
    country_list, country_geo_dict = geoip_lookup(parsed)
    top_three, openweather_candidates = top_three_location(
        country_list, country_geo_dict
    )

    for (country_count, location_info) in itertools.zip_longest(
        top_three.values(), openweather_candidates
    ):
        temperature = get_temp(
            location_info["lat"],
            location_info["lon"],
            args.api_key
        )
        print(f"{location_info['country']} {country_count} {temperature}")


if __name__ == "__main__":
    main()
