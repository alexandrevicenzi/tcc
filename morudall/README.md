# Morudall

This module subscribe to a MQTT Broker and listen for messages from Soressa. Process and store all messages from Soressa.

## Setup

Install all packages:

`pip install -r requirements.txt`

## Extra setup

You also need to setup Redis and MongoDB.

## Run

`python morudall.py`

## Mock Soressa

Run `soressa.py` with a custom `input.gps`.

`python soressa.py <device_id>`
