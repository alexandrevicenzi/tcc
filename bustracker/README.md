# BusTracker

The main Web application to check where your bus is.

## Setup

Install all packages:

`pip install -r requirements.txt`

Create the DB:

`./manage.py migrate`

Create Admin user:

`./manage.py createsuperuser`

## Development

To run local:

`./manage.py runserver 0.0.0.0:8000`

You also need to setup Redis and MongoDB.

## Release

TODO
