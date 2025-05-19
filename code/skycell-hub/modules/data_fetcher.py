import json
from datetime import datetime
import os

def intakeLoRA(lora_data):
    """
    lora_data: dict with keys matching the required fields, or containing raw LoRa data to be mapped.
    """
    # Map or extract fields as needed
    balloon_state = {
        "altitude": lora_data.get("altitude", 0),
        "latitude": lora_data.get("latitude", 0.0),
        "longitude": lora_data.get("longitude", 0.0),
        "temperature": lora_data.get("temperature", 3.0),
        "signal_strength": lora_data.get("signal_strength", 0),
        "bandwidth": lora_data.get("bandwidth", 0),
        "barometric": lora_data.get("barometric", 0),
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "battery": lora_data.get("battery", 0),
        "interference": lora_data.get("interference", 0)
    }

    os.makedirs('data', exist_ok=True)
    with open('data/balloon_state.json', 'w') as f:
        json.dump(balloon_state, f, indent=2)