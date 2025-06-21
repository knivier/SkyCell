from machine import Pin, I2C
import time
from aht21 import AHT21

# Adjust pins if needed!
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)

sensor = AHT21(i2c)

while True:
    try:
        temp, hum = sensor.read()
        print("Temperature:", temp, "°C | Humidity:", hum, "%")
    except Exception as e:
        print("Sensor error:", e)
    time.sleep(2)

