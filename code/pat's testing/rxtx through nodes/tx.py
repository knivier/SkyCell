import time
from meshtastic.serial_interface import SerialInterface

iface = SerialInterface("COM13")
destination_id = "no screen protector"  # Replace with the actual node ID of the receiver

def send_with_ack(message, destination_id, timeout=5, retries=3):
    for attempt in range(retries):
        print(f"Sending: {message} (try {attempt + 1})")
        packet = iface.sendText(message, destinationId=destination_id)
        ack = iface.waitForAck(packet["id"], timeout)
        if ack:
            print("✅ ACK received")
            return True
        else:
            print("❌ No ACK, retrying...")
    return False

start_time = time.time()
msg_count = 0

while time.time() - start_time < 10:
    msg = f"msg {msg_count}"
    send_with_ack(msg, destination_id)
    msg_count += 1
    time.sleep(0.2)  # Short delay between attempts (adjustable)

iface.close()
