from machine import I2C, UART, Pin
from bmp180 import BMP180
import time
# Goes thru UART and returns values
# Setup I2C and BMP180
i2c = I2C(1, scl=Pin(15), sda=Pin(14))  # GP15=SCL, GP14=SDA
bmp = BMP180(i2c)
bmp.oversample_sett = 2
bmp.sea_level_pressure = 101325

# Setup UART
uart = UART(0, baudrate=9600, tx=Pin(0))  # TX pin to RX of other Pico

def clamp(val):
    return max(-128, min(127, val))

while True:
    bmp.measure()
    temp = int(bmp.temperature)                          # °C, e.g., 28
    pressure = int(bmp.pressure / 1000)                  # 99041 → 99
    altitude = int(bmp.altitude / 10)                    # 192.94 → 19

    # Clamp to fit signed byte range
    t = clamp(temp)
    p = clamp(pressure)
    a = clamp(altitude)

    output = f"{t},{p},{a}\n"
    uart.write(output)
    time.sleep(1)
