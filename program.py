import os
import time
import smbus2
import requests

from aws import getApiUrl

SENSORMEASUREMENT_TYPE_TEMPERATURE = 2
SENSORMEASUREMENT_TYPE_HUMIDITY = 3


def main():
    # Get environment variables
    testMode = os.getenv('SENSOR_TEST_MODE')  # If True then fake data is used
    location = os.getenv('SENSOR_LOCATION_ID')

    # Get API URL from AWS SSM Parameter Store
    API_URL = getApiUrl()
    print("API_URL: %s" % API_URL)

    if not testMode:
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
        celsTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
        fahrTemp = celsTemp * 1.8 + 32

    else:
        humidity = 90.0
        fahrTemp = 76.45
        celsTemp = 24.5

    print("Relative Humidity is : %.2f %%" % humidity)
    print("Temperature in Celsius is : %.2f C" % celsTemp)
    print("Temperature in Fahrenheit is : %.2f F" % fahrTemp)

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # POST request with SensorMeasurementTypeId 2 (temperature)
    print(API_URL + "/v1/measurements")

    data = {'LocationId': location,
            'value': fahrTemp,
            'SensorMeasurementTypeId': SENSORMEASUREMENT_TYPE_TEMPERATURE,
            'timestamp': timestamp}
    r = requests.post(API_URL+"/v1/measurements", json = data)

    # POST request with SensorMeasurementTypeId 3 (humidity)
    data = {'LocationId': location,
            'value': humidity,
            'SensorMeasurementTypeId': SENSORMEASUREMENT_TYPE_HUMIDITY,
            'timestamp': timestamp}
    r = requests.post(API_URL+"/v1/measurements", json = data)


if __name__ == "__main__":
    main()
