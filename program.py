import os
import time
import smbus2
import requests
import sentry_sdk

from aws import get_secret

SENSORMEASUREMENT_TYPE_TEMPERATURE = 2
SENSORMEASUREMENT_TYPE_HUMIDITY = 3


def main():

    SENTRY_URL = get_secret("SENTRY_URL")
    print(SENTRY_URL)
    sentry_sdk.init(
        dsn=SENTRY_URL,
        traces_sample_rate=1.0
    )

    # Get environment variables
    test_mode = os.getenv('SENSOR_TEST_MODE')  # If True then fake data is used
    location = os.getenv('SENSOR_LOCATION_ID')

    # Get API URL from AWS SSM Parameter Store
    api_url = get_secret("API_URL")
    print(f'API_URL: {api_url}')

    if not test_mode:
        bus = smbus2.SMBus(1)
        bus.write_byte(0x40, 0xF5)

        time.sleep(0.3)

        # SI7021 address, 0x40  Read 2 bytes, Humidity
        data0 = bus.read_byte(0x40)
        data1 = bus.read_byte(0x40)

        # Convert the data
        humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6

        time.sleep(0.3)
        bus.write_byte(0x40, 0xF3)
        time.sleep(0.3)

        # SI7021 address, 0x40 Read data 2 bytes, Temperature
        data0 = bus.read_byte(0x40)
        data1 = bus.read_byte(0x40)

        # Convert the data and output it
        temp_celcius = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
        temp_fahrenheit = temp_celcius * 1.8 + 32

    else:
        humidity = 90.0
        temp_fahrenheit = 76.45
        temp_celcius = 24.5

    print(f'Relative Humidity: {humidity}')
    print(f'Temperature in Celsius: {temp_celcius}')
    print(f'Temperature in Fahrenheit: {temp_fahrenheit} F')

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # POST request with SensorMeasurementTypeId 2 (temperature)
    print(api_url + "/v1/measurements")

    data = {'LocationId': location,
            'value': temp_fahrenheit,
            'SensorMeasurementTypeId': SENSORMEASUREMENT_TYPE_TEMPERATURE,
            'timestamp': timestamp}
    result = requests.post(api_url + "/v1/measurements", json=data)

    # POST request with SensorMeasurementTypeId 3 (humidity)
    data = {'LocationId': location,
            'value': humidity,
            'SensorMeasurementTypeId': SENSORMEASUREMENT_TYPE_HUMIDITY,
            'timestamp': timestamp}
    result2 = requests.post(api_url + "/v1/measurements", json=data)


if __name__ == "__main__":

    main()
