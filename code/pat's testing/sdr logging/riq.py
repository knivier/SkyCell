import os
import subprocess
import time

# Parameters
start_freq = 26_000_000       # 24 MHz
end_freq = 1_500_000_000      # 1.5 GHz
step_freq = 2_000_000         # 2.4 MHz (max sample rate of RTL-SDR)
sample_rate = 2_400_000       # 2.4 MSPS
duration_sec = 0.1            # 100 ms
samples = int(sample_rate * duration_sec)
gain = 0                     # Adjust as needed TODO: ADJUST GAIN TO SEE NOISE FLOOR BETTER
output_dir = "iq_data"

os.makedirs(output_dir, exist_ok=True)

print(f"[+] Starting sweep from {start_freq / 1_000_000:.3f} MHz to {end_freq / 1_000_000:.3f} MHz with step {step_freq / 1_000_000:.3f} MHz")


for freq in range(start_freq, end_freq + 1, step_freq):
    out_file = os.path.join(output_dir, f"iq_{freq//1_000_000}MHz.iq")
    print(f"[+] Capturing {freq / 1_000_000:.3f} MHz -> {out_file}")

    cmd = [
        "rtl_sdr",
        "-f", str(freq),
        "-s", str(sample_rate),
        "-n", str(samples),
        "-g", str(gain),
        out_file
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"[✓] Successfully captured {freq / 1_000_000:.3f} MHz")
    except subprocess.CalledProcessError as e:
        print(f"[!] rtl_sdr failed at {freq} Hz: {e}")
    
    time.sleep(0.1)  # Optional delay between captures

print("[✓] Sweep complete.")
