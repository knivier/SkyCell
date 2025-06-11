import meshtastic.serial_interface
from pubsub import pub
import time
import os
import json
import ast

interface = meshtastic.serial_interface.SerialInterface("/dev/ttyUSB1")
interface.frequency = int(915e6)  # Replace with your desired frequency
print("Connected to Meshtastic interface\n")

def onReceive(packet, interface):
    print(f"Raw packet received: {packet}")  # Debug: see the full packet structure
    
    if 'decoded' in packet:
        try:
            message_bytes = packet['decoded']['payload']
            message_string = message_bytes.decode('utf-8')
            print(f"Decoded message: {repr(message_string)}")  # Debug: see exact string format
            
            # More flexible telemetry detection
            if ('telemetry' in message_string.lower() or 
                message_string.startswith('{') or 
                message_string.startswith("'")):
                
                print(f"Potential telemetry data: {message_string}") 
                write_telemetry(message_string)
            else:
                print("Not a telemetry message")
                print(f"Received: {message_string}")
                
        except Exception as e:
            print(f"Error decoding message: {e}")
    else:
        print("No 'decoded' field in packet")

# Subscribe to all message types to see what we're actually receiving
pub.subscribe(onReceive, 'meshtastic.receive.text')
# Also try subscribing to telemetry specifically
pub.subscribe(onReceive, 'meshtastic.receive.telemetry')

def write_telemetry(telemetry):
    print(f"write_telemetry called with: {repr(telemetry)}")
    
    # Show current working directory
    current_dir = os.getcwd()
    print(f"📁 Current working directory: {current_dir}")
    
    # Always write to files, regardless of JSON conversion success
    try:
        # Append to log file
        log_file_path = os.path.abspath("telemetry_log.json")
        with open("telemetry_log.json", 'a') as tl:
            tl.write(telemetry + '\n')
            tl.flush()
            os.fsync(tl.fileno())
        print(f"✅ Telemetry data appended to log file: {log_file_path}")
        print(f"📏 Log file size: {os.path.getsize('telemetry_log.json')} bytes")
        
        # Write to current telemetry file
        telemetry_file_path = os.path.abspath("telemetry.json")
        with open("telemetry.json", 'w') as t:
            t.write(telemetry)
            t.flush()
            os.fsync(t.fileno())
        print(f"✅ Telemetry data written to: {telemetry_file_path}")
        print(f"📏 Telemetry file size: {os.path.getsize('telemetry.json')} bytes")
        
    except Exception as e:
        print(f"❌ Failed to write to files: {e}")
        return
    
    # Try to parse and pretty-print JSON (optional, doesn't affect file writing)
    try:
        if telemetry.startswith("'"):
            # Handle single quotes
            telemetry_dict = ast.literal_eval(telemetry)
        else:
            # Handle double quotes
            telemetry_dict = json.loads(telemetry)
        
        telemetry_json = json.dumps(telemetry_dict, indent=2)
        print("✅ Telemetry data converted to JSON:", telemetry_json)
        
        # Write pretty JSON to a separate file
        pretty_file_path = os.path.abspath("telemetry_pretty.json")
        with open("telemetry_pretty.json", 'w') as tp:
            tp.write(telemetry_json)
            tp.flush()
            os.fsync(tp.fileno())
        print(f"✅ Pretty JSON written to: {pretty_file_path}")
        print(f"📏 Pretty file size: {os.path.getsize('telemetry_pretty.json')} bytes")
        
    except Exception as e:
        print(f"⚠️  Could not parse as JSON (but files were still written): {e}")

print("Listening for messages... Press Ctrl+C to stop")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down...")
    interface.close()