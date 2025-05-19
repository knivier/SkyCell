import time
from meshtastic.serial_interface import SerialInterface

iface = SerialInterface("COM13")
print("Connected to", iface)
destination_id = "433e5eb8"  # Replace with the actual node ID of the receiver
print(iface.nodes)

def send_with_ack(message, destination_id, timeout=5, retries=3):
    for attempt in range(retries):
        print(f"Sending: {message} (try {attempt + 1})")
        packet = iface.sendText(message, destinationId=destination_id)
        try:
            # Wait for an ACK or NAK response (with timeout implemented separately)
            ack_packet = iface.waitForAckNak()  

            if ack_packet is not None and ack_packet.id == packet.id:
                print("ACK received for packet id", packet.id)
            else:
                print("No ACK or mismatched ACK received.")
        except all as e:
            print(e)

            continue

    return False

start_time = time.time()
msg_count = 0

while time.time() - start_time < 10:
    msg = f"msg {msg_count}"
    send_with_ack(msg, destination_id)
    msg_count += 1
    time.sleep(0.2)  # Short delay between attempts (adjustable)

iface.close()

import meshtastic.serial_interface
import time

message = "Test Message"
sender_node_id = '433e5eb8'

interface = meshtastic.serial_interface.SerialInterface()

def send_message(message):
    interface.sendText(
        text=message,
        destinationId=sender_node_id,
        wantAck=True,
        wantResponse=True
        )

send_message(message)

while True:
    time.sleep(0.1)