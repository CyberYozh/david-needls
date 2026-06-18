import requests
import socket
import whois
import json


def dns_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"[DNS] IP Address: {ip}")
    except Exception as e:
        print(f"[DNS] Error: {e}")


def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        print("\n[WHOIS] Info:")
        print(f"Registrar: {w.registrar}")
        print(f"Creation Date: {w.creation_date}")
        print(f"Expiration Date: {w.expiration_date}")
        print(f"Country: {w.country}")
    except Exception as e:
        print(f"[WHOIS] Error: {e}")


def headers_check(domain):
    try:
        url = f"http://{domain}"
        r = requests.get(url, timeout=5)
        print("\n[HEADERS]")
        for k, v in r.headers.items():
            print(f"{k}: {v}")
    except Exception as e:
        print(f"[HEADERS] Error: {e}")


def status_check(domain):
    try:
        url = f"http://{domain}"
        r = requests.get(url, timeout=5)
        print(f"\n[STATUS] {domain} -> {r.status_code}")
    except Exception as e:
        print(f"[STATUS] Down or blocked: {e}")


def subdomain_check(domain):
    print("\n[SUBDOMAIN CHECK]")
    subdomains = ["www", "mail", "dev", "test", "api", "admin"]
    for sub in subdomains:
        target = f"{sub}.{domain}"
        try:
            socket.gethostbyname(target)
            print(f"Found: {target}")
        except:
            pass

def main():
    target = input("Enter domain (example.com): ").strip()


    dns_lookup(target)
    whois_lookup(target)
    headers_check(target)
    status_check(target)
    subdomain_check(target)

    print("\n--- DONE ---\n")

if __name__ == "__main__":
    main()
