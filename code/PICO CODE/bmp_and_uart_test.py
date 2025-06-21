from machine import Pin, I2C, UART
from bmp180_driver import BMP180
import time

# Init I2C
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
bmp = BMP180(i2c)

# Init UART
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))  # GP0 TX, GP1 RX

while True:
    temp = bmp.read_temperature()
    press = bmp.read_pressure()
    alt = bmp.read_altitude()

    data_str = "BMP180,{:.2f},{:.2f},{:.2f}\n".format(temp, press, alt)
    uart.write(data_str)  # Send over UART

    time.sleep(2)

