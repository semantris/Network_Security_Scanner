import socket
import threading

def scan_port(ip, port, timeout=0.5):
    """Try to connect to a single port. Returns True if open."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((ip, port))
        return result == 0
    except socket.error:
        return False
    finally:
        sock.close()

def grab_banner(ip, port, timeout=1):
    """Try to read whatever the service sends after connecting."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else None
    except Exception:
        return None

def scan_host(ip, port_range=range(1, 1025), max_threads=100):
    """Scan a range of ports on one host, using a thread pool to stay fast."""
    open_ports = {}
    lock = threading.Lock()
    semaphore = threading.Semaphore(max_threads)  # caps concurrent threads

    def worker(port):
        with semaphore:
            if scan_port(ip, port):
                banner = grab_banner(ip, port)
                with lock:
                    open_ports[port] = banner
                print(f"[+] {ip}:{port} open  {('- ' + banner) if banner else ''}")

    threads = []
    for port in port_range:
        t = threading.Thread(target=worker, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return open_ports


if __name__ == "__main__":
    target = input("Enter target IP: ").strip()
    print(f"\nScanning ports on {target} ...\n")
    results = scan_host(target, range(1, 1025))
    print(f"\nScan complete. {len(results)} open port(s):")
    for port, banner in sorted(results.items()):
        print(f"  - {port}: {banner if banner else '(no banner)'}")