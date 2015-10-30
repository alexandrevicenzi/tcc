# BusTracker

The main Web application to check where your bus is.

## Setup

### Install all packages

`pip install -r requirements.txt`

### Create the DB

`./manage.py migrate`

### Create Admin user

`./manage.py createsuperuser`

You also need to setup Redis and MongoDB.

## Run

### Development

`./manage.py runserver 0.0.0.0:8000`

### Release

TODO

### Site Settings

Before using the Web App you need to go to Admin and setup some settings:

| Key | Value |
|-----|-------|
| default_latitude | |
| default_longitude | |
| google_maps_api_key | GoogleMaps API Key |
| api_token | An API Access Token |

#### Required APIs

- Google Maps Directions API
- Google Maps Distance Matrix API
- Google Maps Geocoding API
- Google Maps JavaScript API

[More Info](https://developers.google.com/maps/)
