# A small local "database" mapping service banners/signatures to known CVEs.
# In a real tool this would query the NVD API live — this is the offline,
# explainable version suitable for a school project.

KNOWN_VULNS = {
    "vsftpd 2.3.4": [
        ("CVE-2011-2523", "Backdoor command execution in vsftpd 2.3.4", "Critical")
    ],
    "OpenSSH_7.2p2": [
        ("CVE-2016-6210", "User enumeration via timing attack", "Medium")
    ],
    "OpenSSH_4.7p1": [
        ("CVE-2008-1483", "Weak SSH key generation vulnerability", "High")
    ],
    "Apache/2.2.8": [
        ("CVE-2011-3192", "Range header denial-of-service", "Medium")
    ],
    "ProFTPD 1.3.1": [
        ("CVE-2010-4221", "ProFTPD ASCII file transfer stack buffer overflow", "High")
    ],
    "MySQL": [
        ("CVE-2012-2122", "Authentication bypass via crafted password comparison", "High")
    ],
}


def check_vulnerabilities(banner):
    """Compare a banner string against known vulnerability signatures."""
    if not banner:
        return []

    findings = []
    for signature, vulns in KNOWN_VULNS.items():
        if signature.lower() in banner.lower():
            for cve_id, description, severity in vulns:
                findings.append({
                    "cve": cve_id,
                    "description": description,
                    "severity": severity
                })
    return findings


if __name__ == "__main__":
    # quick manual test
    test_banner = "220 (vsFTPd 2.3.4)"
    print(check_vulnerabilities(test_banner))