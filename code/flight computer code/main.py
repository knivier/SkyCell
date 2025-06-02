import meshtastic.serial_interface
import time

message = "Test Message"

test_telemetry = {
    'telemetry': {
        'battery': 100,
        'temperature': 25,
        'humidity': 50
    }
}
print("Test telemetry: ", test_telemetry)

interface = meshtastic.serial_interface.SerialInterface("/dev/ttyUSB0")
print("Connected to Meshtastic interface\n")

def send_message(message):
    interface.sendText(
        text=message,
        wantAck=True,
        wantResponse=True 
        )

for i in range(500):
    message = f"Message n {i}"

    #send_message(message)
    tx_telemetry = str(test_telemetry)
    send_message(tx_telemetry)
    print("Sent: ", tx_telemetry)
    #print("Sent: ", message)
    time.sleep(3)

interface.close()
exit(0)