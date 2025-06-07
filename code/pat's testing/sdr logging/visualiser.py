
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Config: Choose your file path and name here ---
directory = "/home/patcybermind/Documents/hcprojects/apex/SkyCell/iq_data"  # <-- change this
filename = "iq_100MHz.iq"             # <-- change this
sample_rate = 2.4e6  # Hz
fft_size = 4096
overlap = 0.5

# --- Construct full file path ---
filepath = os.path.join(directory, filename)

# --- Load and normalize IQ data ---
raw = np.fromfile(filepath, dtype=np.uint8)
iq = (raw.astype(np.float32) - 127.5) / 127.5
I = iq[0::2]
Q = iq[1::2]
samples = I + 1j * Q

# --- FFT averaging ---
step = int(fft_size * (1 - overlap))
segments = (len(samples) - fft_size) // step
if segments <= 0:
    raise ValueError("File too short for chosen FFT size and overlap.")

avg_power = np.zeros(fft_size)
for i in range(segments):
    windowed = samples[i*step : i*step + fft_size] * np.hanning(fft_size)
    fft = np.fft.fftshift(np.fft.fft(windowed))
    power = np.abs(fft)**2
    avg_power += power

avg_power /= segments
power_db = 10 * np.log10(avg_power + 1e-12)

# --- Frequency axis ---
freq_axis = np.fft.fftshift(np.fft.fftfreq(fft_size, 1/sample_rate)) / 1e6  # MHz

# --- Plot ---
plt.figure(figsize=(10,6))
plt.plot(freq_axis, power_db)
plt.title(f"Spectrum: {filename}")
plt.xlabel("Frequency (MHz)")
plt.ylabel("Power (dB)")
plt.grid()
plt.tight_layout()
plt.show()
