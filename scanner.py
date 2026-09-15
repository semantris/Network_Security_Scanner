import argparse
import json
from datetime import datetime

from discovery import scan_subnet
from port_scan import scan_host
from vuln_db import check_vulnerabilities


def run_full_scan(subnet, port_range):
    print(f"\n=== Step 1: Host Discovery ({subnet}) ===")
    live_hosts = scan_subnet(subnet)

    if not live_hosts:
        print("No live hosts found. Check your subnet/VM network settings.")
        return {}

    full_report = {}

    for host in live_hosts:
        print(f"\n=== Step 2: Port Scan ({host}) ===")
        open_ports = scan_host(host, port_range)

        host_report = {}
        for port, banner in open_ports.items():
            print(f"\n=== Step 3: Vulnerability Check ({host}:{port}) ===")
            vulns = check_vulnerabilities(banner)
            host_report[port] = {
                "banner": banner,
                "vulnerabilities": vulns
            }
            if vulns:
                for v in vulns:
                    print(f"  !! {v['cve']} ({v['severity']}) - {v['description']}")

        full_report[host] = host_report

    return full_report


def save_report(report, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_report_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved to {filename}")
    return filename


def parse_port_range(port_str):
    """Turn '1-1024' into range(1, 1025)."""
    start, end = port_str.split("-")
    return range(int(start), int(end) + 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simple Python network vulnerability scanner"
    )
    parser.add_argument("--subnet", required=True, help="e.g. 192.168.56.0/24")
    parser.add_argument("--ports", default="1-1024", help="e.g. 1-1024")
    parser.add_argument("--output", default=None, help="Output JSON filename")

    args = parser.parse_args()
    port_range = parse_port_range(args.ports)

    report = run_full_scan(args.subnet, port_range)

    if report:
        save_report(report, args.output)