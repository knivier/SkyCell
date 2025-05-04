import time
import busio # type: ignore
import digitalio # type: ignore
import board # type: ignore
import microcontroller # type: ignore
import adafruit_rfm9x # type: ignore


sleep_time = 0
current_time = 1

while current_time <= sleep_time:
    print("Sleeping for {0} seconds".format(sleep_time - current_time))
    time.sleep(1)
    current_time += 1

RADIO_FREQ_MHZ = 868.0  # Frequency of the radio in Mhz. Must match your

# Create library object using our bus SPI port for radio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# RFM9x Breakout Pinouts
CS = digitalio.DigitalInOut(board.D27)
RESET = digitalio.DigitalInOut(board.D22)

CS.direction = digitalio.Direction.OUTPUT
RESET.direction = digitalio.Direction.OUTPUT

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




# Configure for long range
rfm9x.tx_power = 20
rfm9x.signal_bandwidth = 125000
rfm9x.coding_rate = 5
rfm9x.spreading_factor = 11


sleep_time = 1000
current_time = 0
while current_time <= sleep_time:
    print("continuing for {0} seconds".format(sleep_time - current_time))
    time.sleep(1) #was .5
    current_time += 1
    rfm9x.send(bytes("Hello world!\r\n", "utf-8"))
    print("Sent Hello World message!")
    # print if we got an ack back
    if rfm9x.receive(with_ack=True):
        print("ACK received")
    else:
        print("No ACK received")