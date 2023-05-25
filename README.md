# Environment Sensor

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/9d675e9ee55f4717a0067f7a7ea25742)](https://app.codacy.com/gh/sophiekruijt/home-automation-environment-sensor/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

Python script that collects temperature and humidity data using a Raspberry Pi and a [Si7021 Temperature & Humidity Sensor Breakout Board](https://www.adafruit.com/product/3251).

## Development
1. `pip install -r requirements.txt`
2. `python program.py`

## Unit tests
`python -m unittest discover tests`

## Logging and monitoring

This script is monitored by sentry.io, or SSH into a Raspberry PI to view the logs

## Deployment
SSH into Raspberry Pi's and do a git pull
