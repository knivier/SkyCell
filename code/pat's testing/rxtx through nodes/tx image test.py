

import meshtastic.serial_interface
import time

message = "Test Message"
sender_node_id = '433e5eb8'


interface = meshtastic.serial_interface.SerialInterface("COM13")
print("Connected to Meshtastic interface\n")

def send_message(message):
    interface.sendText(
        text=message,
        destinationId=sender_node_id,
        wantAck=True,
        wantResponse=True 
        )

for i in range(10):
    message = f"Message n {i}"

    send_message(message)
    print("Sent: ", message)
    time.sleep(1)


interface.close()
exit(0)
while True:
    time.sleep(0.1)

