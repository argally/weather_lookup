"""
Log Normalizer Module

This module will parse a sample of apache access logs and return structured data
Objective is to return a list of Host IP entries which match following criteria:

Log entry occurred between Monday - Friday only
Log entry contains one of the following HTTP status codes 500, 502, 503, 504, 505
"""

from collections import namedtuple
import datetime
import re

# Global regex for the common Apache log format.
FORMAT_PATTERN = re.compile(
    r"(?P<host>[\d\.]+)\s"
    r"(?P<identity>\S*)\s"
    r"(?P<user>\S*)\s"
    r"\[(?P<time>.*?)\]\s"
    r'"(?P<request>.*?)"\s'
    r"(?P<status>\d+)\s"
    r"(?P<bytes>\S*)\s"
)

# Global status codes to use as filter criteria
STATUS_CODES = [
    500,
    502,
    503,
    504,
    505,
]

# Global map to convert Month name to its numeric value
MONTH_MAP = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

# Define a nametuple Access to allow access to values using descriptive field names
Access = namedtuple(
    "Access", ["host", "identity", "user", "time", "request", "status", "bytes"]
)


def parse_entries(log_lines):
    """
    Use regular expression names and generator to yield a
    nametuple called Access

    :param log_lines:
    """
    for line in log_lines:
        match = FORMAT_PATTERN.match(line)
        if match:
            yield Access(**match.groupdict())


def timestamp_readable(timestamp):
    """
    Convert an apache log timestamp to a datetime object

    Return day of week as integer corresponding to weekdays
    between Monday and Friday where Monday is 0 and Sunday is 6

    :param timestamp:
    """
    format_time = datetime.datetime(
        int(timestamp[7:11]),
        MONTH_MAP[timestamp[3:6]],
        int(timestamp[0:2]),
    )
    if format_time.weekday() in range(0, 5):
        return format_time


def normalized_result(log_lines):
    """
    Return filtered list of all the host IP
    which result in 5XX error and occur between Monday - Friday.

    :param log_lines:
    """
    parse_src = parse_entries(log_lines)
    return [
        entry.host
        for entry in parse_src
        if int(entry.status) in STATUS_CODES
        if timestamp_readable(entry.time)
    ]
