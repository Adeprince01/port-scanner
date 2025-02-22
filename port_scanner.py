import socket
import threading
from queue import Queue
import time

# Queue for threading
scan_queue = Queue()
open_ports = []

# Function to scan a single port
def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except Exception:
        pass

# Worker function for threading
def worker(target):
    while True:
        try:
            port = scan_queue.get()
            scan_port(target, port)
            scan_queue.task_done()
        except:
            break

# Fill the queue and run the scan
def run_scanner(target, port_range):
    # Populate the queue
    for port in port_range:
        scan_queue.put(port)

    # Start threads (10 for speed)
    thread_count = 10
    for _ in range(thread_count):
        thread = threading.Thread(target=worker, args=(target,))
        thread.daemon = True
        thread.start()

    # Wait for completion
    scan_queue.join()

# Main execution
if __name__ == "__main__":
    # Get target IP from user input
    target = input("Enter the IP address to scan (e.g., 127.0.0.1): ").strip()
    port_range = range(1, 1025)  # Still scanning 1-1024, adjustable later

    print(f"Scanning {target} for open ports...")
    start_time = time.time()

    run_scanner(target, port_range)

    end_time = time.time()
    print(f"Scan completed in {end_time - start_time:.2f} seconds.")
    if open_ports:
        print("Open ports found:", sorted(open_ports))
    else:
        print("No open ports found in the scanned range.")

    # Map common ports to services
    common_services = {21: "FTP", 22: "SSH", 23: "Telnet", 80: "HTTP", 443: "HTTPS"}
    for port in open_ports:
        if port in common_services:
            print(f"Port {port} is open - possible {common_services[port]} service")