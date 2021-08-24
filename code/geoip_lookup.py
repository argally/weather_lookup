"""
GeoIP lookup Country Module

This module will take a list of Host IP address and using MaxMinds GeoLite2-City database
perform a lookup of each Host IP address and return the following two data structures:

A list of Country names
A dictionary of Country names and location data
"""

from collections import Counter
import ipaddress

import geoip2.database
import geoip2.errors

# Global reference to the MaxMinds database file
GEO_IP_DB = "GeoLite2-City.mmdb"


def is_valid_ipv4_address(ip):
    """
    Sanitary check to verify validity of each IP address

    :param ip:
    """
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        try:
            ipaddress.ip_network(ip)
        except ValueError:
            return False
        return True
    return True


def country_data(data):
    """
    For each IP address return corresponding Country Name value
    and standarize to lowercase for later comparison

    If the value doesn't exist return None

    :param data:
    """
    try:
        return data.registered_country.names["en"].lower()
    except KeyError:
        return None


def longitude_data(data):
    """
    For each IP return corresponding longitude value

    If the value doesn't exist return None

    :param data:
    """
    try:
        return data.location.longitude
    except KeyError:
        return None


def latitude_data(data):
    """
    For each IP return corresponding latitude value

    If the value doesn't exist return None

    :param data:
    """
    try:
        return data.location.latitude
    except KeyError:
        return None


def top_three_countries(country_list):
    """
    Use Counter to perform a count on returned list of countries and
    return a new dictionary representing the three countries
    with the highest match

    :param country_list:
    """
    return dict(Counter(country_list).most_common(3))


def top_three_location(country_list, country_dict):
    """
    For the three countries with highest match use a generator method next()
    to step through the country_dict to return first match of country and
    its location data from this dictionary.

    :param country_list:
    :param country_dict:
    """
    top_three = top_three_countries(country_list)
    country_candidates = []
    for country, _ in top_three.items():
        country_candidates.append(
            next(item for item in country_dict if item["country"] == country.lower())
        )
    return top_three, country_candidates


def geoip_lookup(ip_list):
    """
    Open Maxminds database as reader variable and perform lookup
    of each Host IP address.

    Only return positive matches based on valid
    country and valid location data.

    Create a dictionary to store country and location details
    Create a list to store country

    :param ip_list:
    """
    try:
        with geoip2.database.Reader(GEO_IP_DB) as reader:
            country_list = []
            country_geo_dicts = []
            for ip in ip_list:
                if is_valid_ipv4_address(ip):
                    try:
                        response = reader.city(ip)
                        if (
                            country_data(response)
                            and latitude_data(response)
                            and longitude_data(response)
                        ):
                            country_geo_dicts.append(
                                {
                                    "country": country_data(response),
                                    "lat": latitude_data(response),
                                    "lon": longitude_data(response),
                                }
                            )
                            country_list.append(country_data(response))
                    except geoip2.errors.AddressNotFoundError:
                        pass
    except FileNotFoundError:
        print(f"The file {GEO_IP_DB} does not exist")
    return country_list, country_geo_dicts
