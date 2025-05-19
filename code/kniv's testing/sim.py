import cv2
import time
import os
import configparser
from collections import defaultdict

CHUNK_SIZE = 200  # Simulated LoRa packet size
FRAME_ID = 0
frame_buffer = defaultdict(lambda: {"chunks": {}, "total": 0})

# Load settings
def load_settings():
    config = configparser.ConfigParser()
    config.read(r"kniv's testing\sets.ini")
    s = config["Settings"]
    resolution_map = {
        "120": (160, 120),
        "240": (320, 240),
        "360": (480, 360),
        "480": (640, 480),
        "720": (1280, 720)
    }
    res_key = s.get("resolution", "240")
    return {
        "resolution": resolution_map.get(res_key, (320, 240)),
        "interval": 1 / float(s.get("fps", "0.5")),
        "quality_min": int(s.get("quality_min", "6")),
        "quality_max": int(s.get("quality_max", "15")),
        "max_size_bytes": int(s.get("max_file_size_kb", "4")) * 1024
    }

def capture_and_compress(cap, settings):
    ret, frame = cap.read()
    if not ret:
        return None

    width, height = settings["resolution"]
    frame = cv2.resize(frame, (width, height))

    for quality in range(settings["quality_max"], settings["quality_min"] - 1, -1):
        ret, jpeg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        if not ret:
            continue
        jpeg_bytes = jpeg.tobytes()
        if len(jpeg_bytes) <= settings["max_size_bytes"]:
            print(f"[✓] Compressed to {len(jpeg_bytes)} bytes at quality {quality}")
            return jpeg_bytes

    print("[!] Could not compress under max size — skipping frame")
    return None

def send_frame_simulated(jpeg_bytes, frame_id):
    total_chunks = (len(jpeg_bytes) + CHUNK_SIZE - 1) // CHUNK_SIZE
    print(f"[TX] Frame {frame_id} split into {total_chunks} chunks")

    for i in range(total_chunks):
        offset = i * CHUNK_SIZE
        chunk = jpeg_bytes[offset:offset + CHUNK_SIZE]
        packet = bytes([frame_id % 256, i, total_chunks]) + chunk
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
    os.makedirs("imagers/", exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join("imagers/", f"sim_frame_{frame_id}_{timestamp}.jpg")
    with open(filename, "wb") as f:
        f.write(jpeg_bytes)
    print(f"[✓] Reconstructed frame {frame_id} -> {filename}")
    del frame_buffer[frame_id]

def main():
    global FRAME_ID
    settings = load_settings()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not access webcam")
        return

    try:
        while True:
            jpeg = capture_and_compress(cap, settings)
            if jpeg:
                send_frame_simulated(jpeg, FRAME_ID)
                FRAME_ID += 1
            time.sleep(settings["interval"])
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        print("Exiting...")

if __name__ == "__main__":
    main()
