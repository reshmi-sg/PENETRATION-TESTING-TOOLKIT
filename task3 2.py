import socket
import requests
import os
import time

# --------------------- MODULE 1: PORT SCANNER ---------------------
def port_scanner(host, ports=[21, 22, 23, 80, 443, 8080]):
    """
    Scans a host for open ports from the provided list.
    """
    print(f"\n[🔍] Scanning {host} for open ports...")
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((host, port))
                if result == 0:
                    print(f"[OPEN] Port {port} is open")
        except socket.error:
            print(f"[ERROR] Could not connect to {host}")
            return
    print(" Port scan complete.\n")

# --------------------- MODULE 2: BRUTE FORCE LOGIN ---------------------
def brute_force_login(url, username_list, password_list):
    """
    Tries a list of username-password pairs on a Basic Auth protected page.
    """
    print(f"\n Starting brute-force on {url}")
    for username in username_list:
        for password in password_list:
            try:
                response = requests.get(url, auth=(username, password), timeout=5)
                if response.status_code == 200:
                    print(f"[ SUCCESS] Username: {username} | Password: {password}")
                    return
                else:
                    print(f"[-] Failed: {username}:{password}")
            except requests.exceptions.RequestException:
                print("[ERROR] Connection failed or timeout.")
    print("Brute-force failed.\n")

# --------------------- MODULE 3: PING SWEEP ---------------------
def ping_sweep(ip_prefix):
    """
    Pings IPs in a subnet range to check which hosts are online.
    """
    print(f"\n Running ping sweep on {ip_prefix}.0/24")
    for i in range(1, 5):  # Check only 4 IPs for demo
        ip = f"{ip_prefix}.{i}"
        command = f"ping -n 1 {ip} > nul" if os.name == 'nt' else f"ping -c 1 {ip} > /dev/null"
        response = os.system(command)
        if response == 0:
            print(f"[ACTIVE] Host is up: {ip}")
        else:
            print(f"[INACTIVE] Host down: {ip}")
    print(" Ping sweep complete.\n")

# --------------------- MODULE 4: WHOIS LOOKUP ---------------------
def whois_lookup(domain):
    """
    Performs a WHOIS lookup using system command.
    """
    print(f"\n WHOIS Lookup for {domain}")
    try:
        result = os.popen(f"whois {domain}").read()
        print(result[:500])  # Display partial output
    except Exception as e:
        print(f"[ERROR] {e}")
    print(" WHOIS lookup done.\n")

# --------------------- MAIN TOOL MENU ---------------------
def main():
    while True:
        print("\n=== Penetration Testing Toolkit ===")
        print("1. Port Scanner")
        print("2. Brute-Force Login (Basic Auth)")
        print("3. Ping Sweep")
        print("4. WHOIS Lookup")
        print("5. Exit")

        choice = input("Choose a module (1-5): ")

        if choice == '1':
            target = input("Enter host : ")
            port_scanner(target)

        elif choice == '2':
            url = input("Enter login URL : ")
            usernames = ["admin", "user", "test"]
            passwords = ["admin", "1234", "password", "admin123"]
            brute_force_login(url, usernames, passwords)

        elif choice == '3':
            prefix = input("Enter IP prefix (e.g. 192.168.1): ")
            ping_sweep(prefix)

        elif choice == '4':
            domain = input("Enter domain name (e.g. example.com): ")
            whois_lookup(domain)

        elif choice == '5':
            print("Exiting toolkit. ")
            break

        else:
            print("[ERROR] Invalid option. Try again.")

if __name__ == "__main__":
    main()
