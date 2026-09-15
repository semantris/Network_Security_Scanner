import subprocess
import ipaddress


def is_alive(ip):
    """
    Pings a single IP address once, waiting up to 1 second.
    Returns True if the host replies, False otherwise.
    """
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", str(ip)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0


def scan_subnet(subnet):
    """
    Takes a subnet like '192.168.56.0/24' and checks every
    possible host address in it, printing the ones that respond.
    """
    network = ipaddress.ip_network(subnet, strict=False)
    alive_hosts = []

    print(f"Scanning {subnet} ...")
    for ip in network.hosts():
        if is_alive(ip):
            print(f"[+] {ip} is up")
            alive_hosts.append(str(ip))

    return alive_hosts


if __name__ == "__main__":
    # Replace this with your actual lab subnet (check VirtualBox host-only network settings)
    target_subnet = "192.168.56.0/24"
    live_hosts = scan_subnet(target_subnet)

    print("\n--- Scan complete ---")
    print(f"Live hosts found: {len(live_hosts)}")
    for host in live_hosts:
        print(f"  {host}")