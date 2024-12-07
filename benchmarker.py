import subprocess
import json

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def benchmark_miner(miner_name, binary, pool, wallet, worker, max_threads):
    best_hashrate = 0
    best_threads = 0

    for threads in range(1, max_threads + 1):
        print(f"Benchmarking {miner_name} with {threads} threads...")
        try:
            result = subprocess.run(
                [binary, "-v", "-l", pool, "-u", f"{wallet}.{worker}", "-p", "x", "-t", str(threads)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = result.stdout
            hashrate = parse_hashrate(output)
            print(f"{miner_name} - Threads: {threads}, Hashrate: {hashrate} H/s")

            if hashrate > best_hashrate:
                best_hashrate = hashrate
                best_threads = threads
        except Exception as e:
            print(f"Error during benchmarking: {e}")

    return best_threads

def parse_hashrate(output):
    for line in output.split("\n"):
        if "H/s" in line:
            try:
                return float(line.split()[0])
            except ValueError:
                continue
    return 0

def main():
    config = load_config()
    pool = config["pool"]
    wallet = config["wallet"]
    worker = config["worker"]
    max_threads = os.cpu_count()

    best_miner = None
    best_threads = 0
    best_hashrate = 0

    for miner_name, binary in MINER_BINARIES.items():
        if os.path.exists(binary):
            threads = benchmark_miner(miner_name, binary, pool, wallet, worker, max_threads)
            print(f"Best threads for {miner_name}: {threads}")
            if threads > best_threads:
                best_threads = threads
                best_miner = miner_name

    config["algorithm"] = best_miner
    config["threads"] = best_threads
    save_config(config)
    print("Benchmark complete. Updated config.json with optimal settings.")

if __name__ == "__main__":
    main()
