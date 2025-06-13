import numpy as np
import matplotlib.pyplot as plt
import os
import re

# --- Config ---
directory = "/home/patcybermind/Documents/hcprojects/apex/SkyCell/iq_data"
sample_rate = 2.4e6  # Hz
fft_size = 4096
overlap = 0.5
step_hz = 2e6  # center frequency step (not sample rate)

# --- List and sort files by center frequency ---
def extract_freq(filename):
    match = re.search(r"iq_(\d+)MHz\.iq", filename)
    return int(match.group(1)) if match else None

files = sorted(
    [f for f in os.listdir(directory) if f.endswith(".iq") and "iq_" in f],
    key=extract_freq
)

full_freq = []
full_power = []

for i, filename in enumerate(files):
    freq_mhz = extract_freq(filename)
    if freq_mhz is None:
        continue

    filepath = os.path.join(directory, filename)
    raw = np.fromfile(filepath, dtype=np.uint8)
    iq = (raw.astype(np.float32) - 127.5) / 127.5
    I = iq[0::2]
    Q = iq[1::2]
    samples = I + 1j * Q

    step = int(fft_size * (1 - overlap))
    segments = (len(samples) - fft_size) // step
    if segments <= 0:
        print(f"Skipping {filename} (too short)")
        continue

    avg_power = np.zeros(fft_size)
    for j in range(segments):
        windowed = samples[j*step : j*step + fft_size] * np.hanning(fft_size)
        fft = np.fft.fftshift(np.fft.fft(windowed))
        power = np.abs(fft)**2
        avg_power += power

    avg_power /= segments
    power_db = 10 * np.log10(avg_power + 1e-12)
    freq_axis = np.fft.fftshift(np.fft.fftfreq(fft_size, 1/sample_rate)) / 1e6 + freq_mhz

    # Trim 0.2 MHz from both ends to remove overlap (except at spectrum edges)
    if i == 0:
        keep = freq_axis <= (freq_mhz + 1.2)
    elif i == len(files) - 1:
        keep = freq_axis >= (freq_mhz - 1.2)
    else:
        keep = (freq_axis >= (freq_mhz - 1.2)) & (freq_axis <= (freq_mhz + 1.2))

    full_freq.append(freq_axis[keep])
    full_power.append(power_db[keep])

# --- Concatenate all spectra ---
final_freq = np.concatenate(full_freq)
final_power = np.concatenate(full_power)

# --- Plot ---
plt.figure(figsize=(16, 6))
plt.plot(final_freq, final_power, linewidth=0.8)
plt.title("Wideband Spectrum (Stitched from Multiple IQ Files)")
plt.xlabel("Frequency (MHz)")
plt.ylabel("Power (dB)")
plt.grid(True)
plt.tight_layout()
plt.show()
