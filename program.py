import time
import smbus
import requests

# TODO move configuration into a config file
fakeData = False
location = 2

print("Time to measure the temperature")

if not fakeData:
  bus = smbus.SMBus(1)
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
  
print("Relative Humidity is : %.2f %%" %humidity)
print("Temperature in Celsius is : %.2f C" %celsTemp)
print("Temperature in Fahrenheit is : %.2f F" %fahrTemp)

current_time = time.time()
print(current_time)
timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
print("Timestamp %s" %timestamp)

# POST request with SensorMeasurementTypeId 2 (temperature)
data = { 'LocationId':location, 'value':fahrTemp, 'SensorMeasurementTypeId' : 2, 'timestamp':timestamp}
r = requests.post("https://api.sophiekruijt.com/v1/measurements", json=data)

# POST request with SensorMeasurementTypeId 3 (humidity)
data = { 'LocationId':location, 'value':humidity, 'SensorMeasurementTypeId' : 3, 'timestamp':timestamp}
r = requests.post("https://api.sophiekruijt.com/v1/measurements", json=data)
