import meshtastic.serial_interface
from pubsub import pub
import time
import os
import json
import ast  # safer than eval

interface = meshtastic.serial_interface.SerialInterface("COM14")

print("Connected to Meshtastic interface\n")

def onReceive(packet, interface):
    if 'decoded' in packet:
        message_bytes = packet['decoded']['payload']
        message_string = message_bytes.decode('utf-8')
        print("received packet")
        
        # check if the message is a telemetry message
        #check if the message starts with tlm
        if message_string.startswith("{'telemetry'"):
            # extract the telemetry data
            print(f"Telemetry data: {message_string}")
            write_telemetry(message_string)
        else:
            print("Not a telemetry message")
            print(f"Received: {message_string}")

pub.subscribe(onReceive, 'meshtastic.receive.text')


def write_telemetry(telemetry):
    try:
        telemetry_dict = ast.literal_eval(telemetry)
        telemetry_json = json.dumps(telemetry_dict)
        print("Telemetry data converted to JSON:", telemetry_json)
    except Exception as e:
        print("❌ Failed to convert telemetry to JSON:", e)
        return

    with open("telemetry_log.json", 'a') as tl:
        tl.write(telemetry_json + '\n')
        tl.flush()
        os.fsync(tl.fileno())
        print("Telemetry data appended to log file")

    with open("telemetry.json", 'w') as t:
        t.write(telemetry_json)
        t.flush()
        os.fsync(t.fileno())
        print("Telemetry data written to telemetry.json")

    print("Telemetry data written to file")

while True:
    time.sleep(1)