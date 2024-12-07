import json
import os
import subprocess
import threading
import time
from datetime import datetime

# Load configuration
CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{CONFIG_FILE} not found. Please create it.")
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

config = load_config()

# Miner binaries
MINER_BINARIES = {
    "oink70": "./oink70/src/verus",
    "verus_solver": "./verus-solver/nheqminer"
}

# Parameters from config
POOL = config["pool"]
WALLET = config["wallet"]
WORKER = config["worker"]
ALGORITHM = config["algorithm"]
THREADS = config["threads"]
LOG_FILE = config["log_file"]
MONITOR_INTERVAL = config["monitor_interval"]

# Logging function
def log_message(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")
    print(message)

# Miner execution function
def start_mining(miner_name):
    binary = MINER_BINARIES.get(miner_name)
    if not binary or not os.path.exists(binary):
        log_message(f"Error: {miner_name} binary not found. Please run setup.sh.")
        return

    log_message(f"Starting {miner_name} miner...")
    try:
        command = [
            binary,
            "-v", "-l", POOL,
            "-u", f"{WALLET}.{WORKER}",
            "-p", "x",
            "-t", str(THREADS)
        ]
        subprocess.run(command)
    except Exception as e:
        log_message(f"Error running {miner_name}: {e}")

# Monitoring function
def monitor():
    while True:
        log_message("Monitoring miner performance...")
        time.sleep(MONITOR_INTERVAL)

# Main function
def main():
    log_message("Unified Miner Starting...")
    
    if ALGORITHM == "auto":
        # Auto-detect best miner
        log_message("Auto-detecting the best miner...")
        selected_miner = "verus_solver"  # Default to verus_solver, extend to benchmark
    else:
        selected_miner = ALGORITHM

    # Start mining
    miner_thread = threading.Thread(target=start_mining, args=(selected_miner,))
    monitor_thread = threading.Thread(target=monitor)

    miner_thread.start()
    monitor_thread.start()

    miner_thread.join()
    monitor_thread.join()

if __name__ == "__main__":
    main()
