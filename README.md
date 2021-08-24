# weather_lookup

The container performs the following actions:

- Process a specified access log defined in Common Log Format (https://en.wikipedia.org/wiki/Common_Log_Format - sample log attached)
- Extract all lines that resulted in a 5xx error that occured on a weekday (Monday - Friday)
- For these lines, do a country lookup on the remote host IP (MaxMind's GeoLite2 Cities mmdb included for the lookup)
- For the 3 countries with the highest matched linecount perform a weather lookup using the openweathermap API to ascertain the current temperature for the given country (https://openweathermap.org/current API key fe6f82b0341da7b464a08fdb4fba18f4)
- Return the data in the following format in descending order of lines matched
```
<Country Code #1> <Lines Matched> <Temperature in C>
<Country Code #2> <Lines Matched> <Temperature in C>
<Country Code #3> <Lines Matched> <Temperature in C>
```

# Build Python container 

Build Docker image logprocess

```
docker build -t logprocess .
```

## Run the Docker Container

This will run the containter Named logprocessor using image logprocess
By default this will leverage sample.log included with image


```
docker run --name logprocessor logprocess sample.log <openweather_api_key>
```
