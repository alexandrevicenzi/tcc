# BusTracker

The main Web application to check where your bus is.

## Setup

This project requires Python 3.2+.

### venv 3.4

To create a virtualenv with Python 3.4 run:

`virtualenv -p /usr/bin/python3.4 venv`

### Install all packages

`pip install -r requirements.txt`

### Create the DB

`./manage.py migrate`

### Create Admin user

`./manage.py createsuperuser`

### Loading Fixtures

To load settings fixtures:

`./manage.py loaddata apps/settings/fixtures/initial_data.json`

To load core fixtures:

`./manage.py loaddata apps/core/fixtures/initial_data.json`

## Extra setup

You also need to setup Redis and MongoDB.

## Run

### Development

`./manage.py runserver 0.0.0.0:8000`

### Release

TODO

### Dumping DB

Dumping DB to fixtures:

`./manage.py dumpdata <app name> > initial_data.json`

### Site Settings

Before using the Web App you need to go to Admin and setup some settings:

| Key | Value |
|-----|-------|
| default_latitude | |
| default_longitude | |
| google_maps_api_key | GoogleMaps API Key |
| api_token | An API Access Token |

#### Required Google APIs

You need to enable almost all Maps APIs to use BusTracker. The required APIs are:

- Google Maps Directions API
- Google Maps Distance Matrix API
- Google Maps Geocoding API
- Google Maps JavaScript API

[More Info](https://developers.google.com/maps/)
