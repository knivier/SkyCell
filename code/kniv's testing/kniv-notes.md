### Oki doki let's get started

#### What is this?

This is my testing space for projects I'm working on. Timestamps are below

5/11: I created some test beta code for esp-eye transmission stuff

ChatGPT guide below:
Great question, Knivier. Here's **exactly how to test the real ESP-EYE + LoRa system with `receiver.py`** in a full end-to-end setup. I’ll walk you through every step so nothing gets missed:

---

## 🧪 Testing the Real System: ESP Transmitter + PC Receiver

### 🧱 Setup Overview

| Component                             | Role                                      |
| ------------------------------------- | ----------------------------------------- |
| ESP-EYE                               | Captures JPEG, sends over LoRa            |
| LoRa Receiver (e.g. T-Beam or Heltec) | Forwards raw packets to PC via USB serial |
| PC + Python                           | Runs `receiver.py` to reassemble images   |

---

## ✅ Requirements

### On ESP-EYE:

* Your C++ code from earlier
* LoRa module (e.g., SX1276 breakout connected via SPI)
* Antenna attached

### On PC:

* LoRa receiver connected via USB (any LoRa board that supports serial output, like a Heltec/T-Beam/RAK)
* Python + `pyserial` and `Pillow`
* `receiver.py` script

---

## 🧰 Step-by-Step Guide

### 📸 1. Flash the ESP-EYE

1. Use the Arduino IDE or PlatformIO
2. Flash the `esp_camera + LoRa sender` code you already have
3. Use serial monitor to confirm it's sending chunks like:

   ```
   Sent frame 2 (37 chunks)
   ```

---

### 📡 2. Set Up the LoRa Receiver Board

**Goal:** Forward raw LoRa packets over USB serial

If you're using something like a Heltec or T-Beam, use this sketch:

```cpp
#include <SPI.h>
#include <LoRa.h>

#define LORA_SS 18
#define LORA_RST 14
#define LORA_DIO0 26

void setup() {
  Serial.begin(9600);
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);

  if (!LoRa.begin(915E6)) {
    Serial.println("LoRa init failed");
    while (1);
  }

  Serial.println("LoRa Receiver");
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize > 0) {
    while (LoRa.available()) {
      Serial.write(LoRa.read());  // raw binary
    }
    Serial.write('\n');  // delimiter
  }
}
```

> ⚠️ You *must* use `Serial.write()` not `Serial.print()` — this ensures raw binary is passed to `receiver.py`.

---

### 🖥️ 3. Run `receiver.py` on Your PC

Update the port name to match your receiver board:

```python
PORT = '/dev/ttyUSB0'  # Linux
# PORT = 'COM4'        # Windows
```

Run it:

```bash
python receiver.py
```

If everything works, you'll see output like:

```
[✓] Complete frame 2, saving...
frame_2.jpg
```

And the images will appear in the folder!

---

## ✅ Verifying the Test

You’ve confirmed success when:

* The ESP serial monitor shows "Sent frame X"
* The receiver board lights up (DIO0 interrupt)
* `receiver.py` prints "Complete frame X"
* `.jpg` files appear and open cleanly

---

## 🔍 Optional Improvements

* Add checksum in packets for integrity
* Add display preview (Tkinter or OpenCV GUI)
* Add feedback from PC to ESP if frames fail