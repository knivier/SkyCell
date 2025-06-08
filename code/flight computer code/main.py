import meshtastic.serial_interface
import time
from telemetry import Telemetry


run = True

interface = meshtastic.serial_interface.SerialInterface("/dev/ttyUSB0")
print("Connected to Meshtastic interface\n")





def send_message(message):
    interface.sendText(
        text=message,
        wantAck=True,
        wantResponse=True 
        )

telemetry_packet = Telemetry()

while run == True:
    try:
        telemetry_packet.update_readings()
    except Exception as e:
        print("Error updating telemetry readings: ", e)
        telemetry_packet = Telemetry()  # Reset telemetry packet on error

    
    try:
        tx_telemetry = str(telemetry_packet.to_dict())
    except Exception as e:
        print("Error converting telemetry to dict to string: ", e)
        

    try:
        send_message(tx_telemetry)
        print("Sent: ", tx_telemetry)
    except Exception as e:
        print("Attempted to send: ", tx_telemetry)
        print("Error sending telemetry: ", e)

    
    time.sleep(3)

interface.close()
exit(0)

