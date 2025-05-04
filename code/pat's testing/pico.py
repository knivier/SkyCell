# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of sending and receiving data with the RFM95 LoRa radio.
# Author: Tony DiCola
import board # type: ignore
import busio # type: ignore
import digitalio # type: ignore
import time
import adafruit_rfm9x # type: ignore
from adafruit_httpserver import Server, Request, Response, POST
import wifi
import socketpool
import microcontroller

sleep_time = 0
current_time = 1
while current_time <= sleep_time:
    print("Sleeping for {0} seconds".format(sleep_time - current_time))
    time.sleep(1)
    current_time += 1

# Define radio parameters.
RADIO_FREQ_MHZ = 868.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
#CS = digitalio.DigitalInOut(board.GP17)
#RESET = digitalio.DigitalInOut(board.GP6)

CS = digitalio.DigitalInOut(board.GP8)
RESET = digitalio.DigitalInOut(board.GP9)

CS.direction = digitalio.Direction.OUTPUT
RESET.direction = digitalio.Direction.OUTPUT

# Or uncomment and instead use these if using a Feather M0 RFM9x board and the appropriate
# CircuitPython build:
# CS = digitalio.DigitalInOut(board.RFM9X_CS)
# RESET = digitalio.DigitalInOut(board.RFM9X_RST)

# Define the onboard LED
LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT

# Initialize SPI bus.
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16) # first one is sck


# Wait for SPI to be ready
spi.try_lock()


try:
    spi.configure(baudrate=100_000)  # 1 MHz CHANGED
    print("SPI frequency set")
except all:
    print("not set")
finally:
    print("continuing")
    spi.unlock()

# Initialize RFM radio
tries = 0
rfm_connected = False
while (tries < 100) and rfm_connected == False:
    try:
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
        rfm_connected = True
        print("RFM9x: Detected")
    except:
        print("NC")
        tries += 1
        time.sleep(0.02)
if rfm_connected == False:
    print("RFM9x: Not Detected")
    exit(1)

#rfm9x.tx_power = 23
rfm9x.signal_bandwidth = 125000
rfm9x.coding_rate = 5
rfm9x.spreading_factor = 12

# Note that the radio is configured in LoRa mode so you can't control sync
# word, encryption, frequency deviation, or other settings!

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
#rfm9x.high_power = True
#rfm9x.tx_power = 23


# init oled display ssd1306
# import board
# import busio
import adafruit_ssd1306
# init connection
i2c = busio.I2C(board.GP5, board.GP4)
# test
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.text("Hi World", 0, 0, 1)
oled.show()

print("oled code done")






# Send a packet.  Note you can only send a packet up to 252 bytes in length.
# This is a limitation of the radio packet size, so if you need to send larger
# amounts of data you will need to break it into smaller send calls.  Each send
# call will wait for the previous one to finish before continuing.
#sleep_time = 10
#current_time = 0
#while current_time <= sleep_time:
#    print("Sleeping for {0} seconds".format(sleep_time - current_time))
#    time.sleep(.5)
#    current_time += 1
#    rfm9x.send(bytes("Hello world!\r\n", "utf-8"))
#    print("Sent Hello World message!")


rfm9x.agc = True
# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 252 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.
print("Waiting for packets...")


packet_number = 0
while True:
    packet = rfm9x.receive(timeout=2.0, with_ack=True)
    # If you want to receive packets with an acknowledgement, set the with_ack
    # parameter to True.
    # Optionally change the receive timeout from its default of 0.5 seconds:
    # packet = rfm9x.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        # Packet has not been received
        LED.value = False
        
        
    else:
        packet_number += 1
        
        # Received a packet!
        LED.value = True
        # Print out the raw bytes of the packet:
        print("Received (raw bytes): {0}".format(packet))
        # And decode to ASCII text and print it too.  Note that you always
        # receive raw bytes and need to convert to a text format like ASCII
        # if you intend to do string processing on your data.  Make sure the
        # sending side is sending ASCII data before you try to decode!
        packet_text = str(packet, "ascii")
        print("Received (ASCII): {0}".format(packet_text))
        # Also read the RSSI (signal strength) of the last received message and
        # print it.
        rssi = rfm9x.last_rssi
        print("Received signal strength: {0} dB".format(rssi))
        snr = rfm9x.last_snr
        print("Received signal to noise ratio: {0} dB".format(snr))
        oled.fill(0)
        oled.text(packet_text + "\n" + "RSSI: {0} dB \n".format(rssi) + "SNR: {0} dB \n".format(snr) + "packet n: {0} \n".format(packet_number), 0, 0, 1)
        oled.show()

