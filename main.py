import subprocess
import os
import re
import requests
from datetime import datetime

# ----------------------
# CVE Lookup Function
# ----------------------
def search_cves(product_name):
    url = f"https://cve.circl.lu/api/search/{product_name}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            return []
    except Exception as e:
        print(f"Error fetching CVEs: {e}")
        return []

# ----------------------
# Parse Nmap Services
# ----------------------
def parse_nmap_services(nmap_file):
    services = []

    with open(nmap_file, "r") as file:
        lines = file.readlines()

    for line in lines:
        match = re.match(r"(\d+)/tcp\s+open\s+\S+\s+(\S+)\s+([\d\.]+)", line)
        if match:
            port = int(match.group(1))
            service = match.group(2)
            version = match.group(3)
            services.append({
                "port": port,
                "service": service,
                "version": version
            })

    return services

# ----------------------
# Main Scanner
# ----------------------
def main():
    # Target
    target = "23.227.38.65"

    # Create folders
    scan_dir = "scans"
    report_dir = "reports"
    os.makedirs(scan_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    # Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # File paths
    nmap_file = f"{scan_dir}/nmap_results_{timestamp}.txt"
    whatweb_file = f"{scan_dir}/whatweb_results_{timestamp}.txt"
    gobuster_file = f"{scan_dir}/gobuster_results_{timestamp}.txt"
    report_file = os.path.join(report_dir, f"final_report_{timestamp}.txt")

    # --- SCANNING ---
    print("[+] Running Nmap...")
    subprocess.run(["nmap", "-sV", "-T4", "-oN", nmap_file, target])

    print("[+] Running WhatWeb...")
    with open(whatweb_file, "w") as wf:
        subprocess.run(["whatweb", target], stdout=wf)

    print("[+] Running Gobuster...")
    gobuster_wordlist = "/usr/share/seclists/Discovery/Web-Content/common.txt"
    subprocess.run([
        "gobuster", "dir",
        "-u", f"http://{target}",
        "-w", gobuster_wordlist,
        "-o", gobuster_file,
        "-q"
    ])

    # --- PARSING SERVICES ---
    print("[+] Parsing Nmap Services...")
    parsed_services = parse_nmap_services(nmap_file)
    print("Parsed Services:")
    for service in parsed_services:
        print(service)

    # --- CVE LOOKUP ---
    for service in parsed_services:
        print(f"\n[+] Service Found: {service}")
        product = f"{service['service']} {service['version']}"
        cves = search_cves(product)
        if cves:
            print(f"  ↪ Found {len(cves)} CVEs:")
            for cve in cves[:5]:  # Only show top 5
                print(f"    • {cve['id']} - {cve['summary'][:100]}...")
        else:
            print("  ↪ No CVEs found.")

    # --- GENERATE FINAL REPORT ---
    print("[+] Generating Final Report...")
    with open(report_file, "w") as rf:
        rf.write("ELO.SHOPPING VULNERABILITY REPORT\n")
        rf.write("=" * 50 + "\n\n")

        # Add Nmap Results
        if os.path.exists(nmap_file):
            with open(nmap_file, "r") as nf:
                rf.write("NMAP RESULTS:\n")
                rf.write(nf.read() + "\n\n")
        else:
            rf.write("NMAP RESULTS:\nNo data.\n\n")

        # Add WhatWeb Results
        if os.path.exists(whatweb_file):
            with open(whatweb_file, "r") as wf:
                rf.write("WHATWEB RESULTS:\n")
                rf.write(wf.read() + "\n\n")
        else:
            rf.write("WHATWEB RESULTS:\nBlocked or no data.\n\n")

        # Add Gobuster Results
        if os.path.exists(gobuster_file):
            with open(gobuster_file, "r") as gf:
                rf.write("GOBUSTER RESULTS:\n")
                rf.write(gf.read() + "\n\n")
        else:
            rf.write("GOBUSTER RESULTS:\nBlocked or no data.\n\n")

    print(f"[✓] Report saved to {report_file}")

# ----------------------
# Run Script
# ----------------------
if __name__ == "__main__":
    main()
