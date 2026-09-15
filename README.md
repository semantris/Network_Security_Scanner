# Network_Security_Scanner
# Network Vulnerability Scanner

A Python command-line tool that discovers live hosts on a network, scans them for open ports, grabs service banners, and checks those banners against a small database of known CVEs. Built from scratch (no Nmap/OpenVAS dependency) to demonstrate an understanding of the underlying scanning mechanisms for an academic project.

## Features

- **Host discovery** — ping sweep across a subnet (`discovery.py`)
- **Port scanning** — multi-threaded TCP connect scan (`port_scan.py`)
- **Banner grabbing** — reads service version strings from open ports
- **Vulnerability matching** — compares banners against known CVE signatures (`vuln_db.py`)
- **Reporting** — outputs a timestamped JSON report (`scanner.py`)

## Requirements

- Python 3.8+
- Windows, macOS, or Linux (no external/third-party packages — standard library only)

## Project Structure

```
network-scanner/
├── scanner.py       # Main entry point — orchestrates the full scan
├── discovery.py      # Host discovery (ping sweep)
├── port_scan.py       # Port scanning + banner grabbing
├── vuln_db.py          # Known vulnerability signatures + matching logic
└── README.md
```

## Setup

```powershell
# 1. Clone/copy the project folder, then move into it
cd network-scanner

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# No pip installs needed — only standard library modules are used
```

## Usage

```powershell
python scanner.py --subnet <SUBNET> --ports <PORT_RANGE> [--output <FILENAME>]
```

**Arguments:**

| Flag | Required | Description | Example |
|------|----------|-------------|---------|
| `--subnet` | Yes | Target subnet in CIDR notation | `192.168.56.0/24` |
| `--ports` | No (default `1-1024`) | Port range to scan | `1-65535` |
| `--output` | No (default auto-timestamped) | Output JSON filename | `report.json` |

**Example:**

```powershell
python scanner.py --subnet 192.168.56.0/24 --ports 1-1024
```

## Output

The scan prints live progress through three stages (discovery → port scan → vulnerability check) and writes a JSON report, e.g. `scan_report_20260915_143210.json`:

```json
{
  "192.168.56.101": {
    "21": {
      "banner": "220 (vsFTPd 2.3.4)",
      "vulnerabilities": [
        {
          "cve": "CVE-2011-2523",
          "description": "Backdoor command execution in vsftpd 2.3.4",
          "severity": "Critical"
        }
      ]
    }
  }
}
```

## Home Lab Setup

This tool is intended to be tested only against systems you own or are explicitly authorized to test.

- **Scanner**: run from your host machine or a dedicated VM
- **Target**: [Metasploitable2](https://sourceforge.net/projects/metasploitable/) — an intentionally vulnerable VM built for this exact purpose
- **Network**: place both on a VirtualBox Host-Only or Bridged network (not NAT) so they can reach each other

## How It Works (Pipeline)

1. `discovery.py` pings every address in the given subnet to find live hosts (threaded for speed)
2. `port_scan.py` attempts a TCP connect to each port on each live host, then grabs the banner from any open port
3. `vuln_db.py` checks each banner against a local table of known CVE signatures
4. `scanner.py` ties all three stages together and writes the combined results to a JSON report

## Disclaimer

**For educational and authorized testing purposes only.** Scanning networks or systems without explicit permission is illegal in most jurisdictions. Only use this tool against your own infrastructure or systems you have written authorization to test.

## Roadmap / Possible Extensions

- Live CVE lookups via the NVD API instead of a static local table
- UDP scanning support
- CSV/HTML report export
- OS fingerprinting
