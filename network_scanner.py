import nmap
import datetime
import os
import sys
import ipaddress

def check_root():
    """check the script if it run in  root (important for SYN Scan)"""
    if os.geteuid() != 0:
        print("[!] Error: This script must be run with root privileges! Use 'sudo python3 network_scanner.py'")
        sys.exit(1)

def scan_network(target_ip):
    print(f"[*] Starting Nmap SYN Stealth Scan (-sS -sV) on target: {target_ip}")
    scanner = nmap.PortScanner()
    
    try:
        # -sS = SYN Stealth Scan, -sV = Service Version Detection, -F = Fast Scan (Top 100 ports)
        scanner.scan(hosts=target_ip, arguments='-sS -sV -F')
    except Exception as e:
        print(f"[!] Scan failed due to an error: {e}")
        return None

    return scanner

def generate_html_report(scanner, target_ip):
    """Save the result Like HTML Dashboard """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Network Reconnaissance Report - {target_ip}</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; }}
            .container {{ max-width: 950px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; }}
            .meta {{ margin-bottom: 20px; padding: 10px; background: #eef2f3; border-radius: 5px; color: #333; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
            th {{ background-color: #007bff; color: white; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
                tr.risk-high td {{ 
                background-color: #ffe6e6 !important; 
                border-color: #ff9999 !important; 
                color: #990000; 
                font-weight: bold; 
        }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Network Scanner & Vulnerability Recon Report</h1>
            <div class="meta">
                <p><strong>Target IP / Subnet:</strong> {target_ip}</p>
                <p><strong>Scan Timestamp:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Scan Configuration:</strong> Nmap SYN Stealth Scan (-sS) with Service Version Detection (-sV)</p>
            </div>
            <table>
                <tr>
                    <th>Host / IP</th>
                    <th>Port</th>
                    <th>Protocol</th>
                    <th>State</th>
                    <th>Detected Service & Version</th>
                </tr>
    """
    
    hosts_found = False
    for host in scanner.all_hosts():
        hosts_found = True
        hostname = scanner[host].hostname() or "Unknown"
        for proto in scanner[host].all_protocols():
            for port in sorted(scanner[host][proto].keys()):
                state = scanner[host][proto][port]['state']
                service = scanner[host][proto][port]['name']
                product = scanner[host][proto][port].get('product', '')
                version = scanner[host][proto][port].get('version', '')
                service_info = f"{service} ({product} {version})".strip()
                
                # Mark the High Risk  Ports (FTP, Telnet,Http,Https, SMB, RDP) 
                risk_class = "risk-high" if port in [21, 23, 80, 443, 445, 3389] else ""
                
                html_content += f"""
                <tr class="{risk_class}">
                    <td>{host} ({hostname})</td>
                    <td>{port}</td>
                    <td>{proto.upper()}</td>
                    <td>{state}</td>
                    <td>{service_info}</td>
                </tr>
                """

    if not hosts_found:
        html_content += """
        <tr>
            <td colspan="5" style="text-align: center; color: #777;">No active hosts or open ports found.</td>
        </tr>
        """

    html_content += """
            </table>
        </div>
    </body>
    </html>
    """
    
    filename = f"scan_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"[+] HTML Report generated successfully: {filename}")

if __name__ == "__main__":
    # 1. Getting the Root permission 
    check_root()
    
    # 2. Getting the Target from user
    target = input("Enter Target IP or Subnet (e.g., 127.0.0.1 or 192.168.1.0/24): ").strip()
    
    # 3. IP Address Validation (identify the wrong ip address)
    try:
        ipaddress.ip_network(target, strict=False)
    except ValueError:
        print("[!] Error: Invalid IP address or network range provided!")
        sys.exit(1)
        
    # 4. Scan and make the report
    scanner_obj = scan_network(target)
    if scanner_obj:
        generate_html_report(scanner_obj, target)
