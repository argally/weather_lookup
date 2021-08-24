# set base image (host OS)
FROM python:3.9-slim-buster

# set the working directory in the container
WORKDIR /app

# Copy Pip package requirements to working directory
COPY requirements.txt requirements.txt

# Execute pip3 to install modules into image
RUN pip3 install -r requirements.txt

# copy the content of the local code directory to the working directory
COPY code/ .

# command to run on container start
ENTRYPOINT [ "python", "./weather_lookup.py" ]