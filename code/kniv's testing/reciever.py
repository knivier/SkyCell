import serial
import time
import os
from collections import defaultdict

# CONFIG
PORT = '/dev/ttyUSB0'  # Or 'COM3' on Windows
BAUDRATE = 9600

# Setup
ser = serial.Serial(PORT, BAUDRATE, timeout=1)
buffer = defaultdict(lambda: {"chunks": {}, "total": 0, "last_time": time.time()})

def try_save_frame(frame_id):
    data = buffer[frame_id]
    chunks = data["chunks"]
    total = data["total"]

    if len(chunks) == total:
        print(f"[✓] Complete frame {frame_id}, saving...")
        frame_bytes = b''.join(chunks[i] for i in range(total))
        with open(f"frame_{frame_id}.jpg", "wb") as f:
            f.write(frame_bytes)
        del buffer[frame_id]
    else:
        print(f"[ ] Frame {frame_id} incomplete: {len(chunks)}/{total}")

def parse_packet(packet):
    if len(packet) < 3:
        return

    frame_id = packet[0]
    chunk_index = packet[1]
    total_chunks = packet[2]
    payload = packet[3:]

    frame = buffer[frame_id]
    frame["chunks"][chunk_index] = payload
    frame["total"] = total_chunks
    frame["last_time"] = time.time()

    try_save_frame(frame_id)

def main():
    print("Listening for packets...")
    while True:
        if ser.in_waiting:
            packet = ser.read_until(expected=b'\n', size=255)
            parse_packet(bytearray(packet.strip()))
        else:
            time.sleep(0.05)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
