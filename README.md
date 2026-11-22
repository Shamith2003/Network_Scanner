# 🛡️ Automated Python Nmap Network Scanner & HTML Reporter

A Python-based network reconnaissance tool built with python-nmap that automates Nmap SYN stealth scans (-sS) with service version detection (-sV), validates target IP addresses/subnets, highlights high-risk ports, and generates a clean HTML report.

## ✨ Features

- *Root Privilege Check:* Verifies root (sudo) privileges before running raw-socket SYN scans.
- *Input Validation:* Validates target IP addresses and CIDR subnets using Python's ipaddress module.
- *SYN Stealth & Service Scan:* Executes Nmap -sS -sV -F scans to identify open ports and service/version details.
- *High-Risk Port Highlighting:* Automatically highlights ports 21, 23, 80, 443, 445, and 3389 in the HTML report.
- *HTML Report Generation:* Saves a timestamped HTML report (scan_report_YYYYMMDD_HHMMSS.html) for easy viewing in a browser.

## 🛠️ Prerequisites

- *OS:* Linux (tested on Kali Linux)
- *Tools:* nmap and Python 3
- *Python Library:* python-nmap (python3-nmap)

## 📦 Installation

1. Clone the repository:
   bash
   git clone [https://github.com/Shamith2003/Network_Scanner.git](https://github.com/Shamith2003/Network_Scanner.git)
   cd Network_Scanner
   

2. Install Nmap and the Python binding (via apt on Debian/Kali):
   bash
   sudo apt update && sudo apt install nmap python3-nmap -y
   

## 🚀 Usage

Run the script with sudo so -sS (SYN stealth scan) can operate properly:

bash
sudo python3 network_scanner.py


When prompted, enter a target IP address or subnet (for example, 127.0.0.1 or 192.168.8.1). Once complete, an HTML report file will be created in the working directory and can be opened in any web browser.

## ⚠️ Disclaimer

This tool is intended strictly for authorized security testing, learning, and network administration on systems you own or have explicit permission to scan.
