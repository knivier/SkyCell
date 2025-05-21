

import meshtastic.serial_interface
import time

message = "Test Message"
sender_node_id = '433e5eb8'

test_telemetry = {
    'telemetry': {
        'battery': 100,
        'temperature': 25,
        'humidity': 50
    }
}
print("Test telemetry: ", test_telemetry)

interface = meshtastic.serial_interface.SerialInterface("COM13")
print("Connected to Meshtastic interface\n")

def send_message(message):
    interface.sendText(
        text=message,
        destinationId=sender_node_id,
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
while True:
    time.sleep(0.1)

