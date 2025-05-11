import cv2
import time
import os
from collections import defaultdict

FRAME_ID = 0
CHUNK_SIZE = 200
INTERVAL = 2  # seconds

# Simulated LoRa buffer
frame_buffer = defaultdict(lambda: {"chunks": {}, "total": 0})

def capture_and_compress(cap):
    ret, frame = cap.read()
    if not ret:
        return None
    # Resize and compress
    frame = cv2.resize(frame, (160, 120))
    ret, jpeg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    return jpeg.tobytes() if ret else None

def send_frame_simulated(jpeg_bytes, frame_id):
    total_chunks = (len(jpeg_bytes) + CHUNK_SIZE - 1) // CHUNK_SIZE
    print(f"[TX] Frame {frame_id} split into {total_chunks} chunks")
    
    for i in range(total_chunks):
        offset = i * CHUNK_SIZE
        chunk = jpeg_bytes[offset:offset + CHUNK_SIZE]
        packet = bytes([frame_id, i, total_chunks]) + chunk
        receive_packet_simulated(packet)

def receive_packet_simulated(packet):
    frame_id = packet[0]
    chunk_id = packet[1]
    total_chunks = packet[2]
    payload = packet[3:]

    frame = frame_buffer[frame_id]
    frame["chunks"][chunk_id] = payload
    frame["total"] = total_chunks

    if len(frame["chunks"]) == total_chunks:
        reconstruct_frame(frame_id)

def reconstruct_frame(frame_id):
    chunks = frame_buffer[frame_id]["chunks"]
    total = frame_buffer[frame_id]["total"]
    jpeg_bytes = b''.join(chunks[i] for i in range(total))
    os.makedirs("imagers/images", exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join("imagers/images", f"sim_frame_{frame_id}_{timestamp}.jpg")
    with open(filename, "wb") as f:
        f.write(jpeg_bytes)
    print(f"[✓] Reconstructed frame {frame_id} -> {filename}")
    del frame_buffer[frame_id]

def main():
    global FRAME_ID
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not access webcam")
        return

    try:
        while True:
            jpeg = capture_and_compress(cap)
            if jpeg:
                send_frame_simulated(jpeg, FRAME_ID)
                FRAME_ID += 1
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        print("Exiting...")

if __name__ == "__main__":
    main()
