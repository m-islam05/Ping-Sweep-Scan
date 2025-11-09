# Ping Sweep (for a full subnet).

# Imported Libraries.
import subprocess
import platform

def ping_sweep(subnet_base, start_host, end_host):
    
    # Determine platform-specific ping argument for count/number of packets
    system = platform.system().lower()
    if system == "windows":
        count_flag = "-n"      # Windows uses -n <count>
    else:
        count_flag = "-c"      # Unix-like uses -c <count>

    # Ensure start <= end
    if start_host > end_host:
        start_host, end_host = end_host, start_host

    # Loop through the numeric host range and ping each IP
    for host in range(start_host, end_host + 1):            # +1 to include end_host
        ip = f"{subnet_base}.{host}"                        # Build full IP address
        try:
            # Run ping once; suppress output, check return code only
            result = subprocess.run(
                ["ping", count_flag, "1", ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=3
            )
            if result.returncode == 0:
                print(f"Host {ip} is active")
        except subprocess.TimeoutExpired:
            # Treat timeout as host not responding
            pass
        except Exception as e:
            # Other unexpected errors (e.g., permission issues)
            print(f"Error pinging {ip}: {e}")



# ---------------- MAIN ---------------- #

# Get base subnet (everything before the last octet)
subnet_base = input("Enter subnet base (e.g., 192.168.1): ").strip() or "192.168.1"

# Get start & end host numbers and validate they are integers 0-255
try:
    start_ip = int(input("Enter starting host number (0-255): ").strip() or "1")
    end_ip = int(input("Enter ending host number (0-255): ").strip() or "254")
except ValueError:
    print("Invalid input: start and end must be integers.")
    raise SystemExit(1)

if not (0 <= start_ip <= 255 and 0 <= end_ip <= 255):
    print("Host numbers must be between 0 and 255.")
    raise SystemExit(1)

# Call function 
print(f"\nScanning {subnet_base}.{start_ip} through {subnet_base}.{end_ip} ...\n")
ping_sweep(subnet_base, start_ip, end_ip)
print("\n--- Complete ---")
