import os
import subprocess
import time

def write_sweep_number(sweep_number):
    try:
        with open("last_sweep_number.txt", "w") as f:
            f.write(str(sweep_number))
    except Exception as e:
        print(f"Error writing sweep number: {e}")


def run_sweep(currrent_sweep_number):
    # Parameters
    start_freq = 30_000_000       # 24 MHz
    end_freq = 1_500_000_000      # 1.5 GHz
    step_freq = 2_000_000         # 2.4 MHz (max sample rate of RTL-SDR)
    sample_rate = 2_400_000       # 2.4 MSPS
    duration_sec = 0.07            # 100 ms
    samples = int(sample_rate * duration_sec)
    gain = 0                  # Adjust as needed TODO: ADJUST GAIN TO SEE NOISE FLOOR BETTER 30
    output_dir = "iq_data"
    os.makedirs(output_dir, exist_ok=True)

    print(f"Starting sweep {currrent_sweep_number} from {start_freq / 1_000_000:.3f} MHz to {end_freq / 1_000_000:.3f} MHz with step {step_freq / 1_000_000:.3f} MHz")


    for freq in range(start_freq, end_freq + 1, step_freq):
        out_file = os.path.join(output_dir, f"iq_{currrent_sweep_number}_{freq//1_000_000}MHz.iq")
        print(f"Capturing {freq / 1_000_000:.3f} MHz -> {out_file}")

        cmd = [
            "rtl_sdr",
            "-f", str(freq),
            "-s", str(sample_rate),
            "-n", str(samples),
            "-g", str(gain),
            out_file
        ]

        try:
            subprocess.run(cmd, check=True, timeout=5)
            print(f"Successfully captured {freq / 1_000_000:.3f} MHz")
        except Exception as e:
            print(f"rtl_sdr failed at {freq} Hz: {e}")
            time.sleep(2)  # Add a longer delay after failure


        time.sleep(0.1)  # Optional delay between captures

    print("Sweep complete.")

def get_current_sweep_number():
    try:
        with open("last_sweep_number.txt", "r") as f:
            last_sweep_number = f.read().strip()
        if not last_sweep_number:
            last_sweep_number = 0
        return int(last_sweep_number)
    except Exception as e:
        print(f"Error reading last sweep number: {e}")
        return 0

def get_uptime():
    try:
        with open("/proc/uptime", "r") as uptime_file:
            uptime = uptime_file.read().strip()
        return uptime.split()[0]  # Return the first part which is the uptime in seconds
    except Exception as e:
        print(f"Error reading uptime: {e}")
        return 3737

def log_sweep_number_uptime(sweep_number, uptime):
    try:
        with open("sweep_log.txt", "a") as log_file:
            log_file.write(f"Sweep Number: {sweep_number}, Uptime: {uptime} seconds\n")
    except Exception as e:
        print(f"Error logging sweep number and uptime: {e}")



current_sn = get_current_sweep_number()

new_sweep_number = get_current_sweep_number() + 1
write_sweep_number(new_sweep_number) 

run_sweep(current_sn)  # Initial sweep to start with
print("ran sdr sweep number: ", current_sn)
log_sweep_number_uptime(current_sn, get_uptime())



interval_seconds = 6 * 60  # Run sweeps every 100 seconds
while True:
    for i in range(0, interval_seconds):  
        time.sleep(1)  
    current_sn = get_current_sweep_number()
    print(f"Running sweep number: {current_sn} uptime: {get_uptime()} seconds")
    log_sweep_number_uptime(get_current_sweep_number(), get_uptime())
    new_sweep_number = get_current_sweep_number() + 1
    write_sweep_number(new_sweep_number) 
    try:
        run_sweep(current_sn)  # Run the sweep
        print("ran sweep...") 
    except Exception as e:
        print(f"Error during sweep: {e}")
        
    
    

    
    print(f"Sweep completed. Uptime: {get_uptime()} seconds") 
    

    
    
    