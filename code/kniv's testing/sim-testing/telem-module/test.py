from machine import Pin, I2C
from bmp180_driver import BMP180
import time

i2c = I2C(0, scl=Pin(5), sda=Pin(4))  # Change pins if needed
bmp = BMP180(i2c)

while True:
    temp = bmp.read_temperature()
    press = bmp.read_pressure()
    alt = bmp.read_altitude()
    
    print("Temp (C):", temp)
    print("Pressure (Pa):", press)
    print("Altitude (m):", alt)
    time.sleep(2)

