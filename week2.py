import socket
from dns import resolver, exception
import json

# Subdomain listesi (örnek veya harici bir dosyadan alınabilir)
subdomains = [
    "www", "mail", "accounts", "blog", "shop", "cdn", "api", "test", "dev"
]

def check_subdomain(domain):
    """
    Belirtilen domain için geçerli ve geçersiz subdomainleri kontrol eder.
    """
    valid_subdomains = []
    invalid_subdomains = []
    
    for sub in subdomains:
        subdomain = f"{sub}.{domain}"
        try:
            # DNS A kaydını sorgula
            ip = socket.gethostbyname(subdomain)
            valid_subdomains.append({"subdomain": subdomain, "ip": ip})
        except socket.gaierror:
            invalid_subdomains.append({"subdomain": subdomain, "error": "No DNS record found"})
    
    return valid_subdomains, invalid_subdomains

def get_dns_records(subdomain):
    """
    Geçerli bir subdomainin DNS kayıtlarını sorgular (A, CNAME, MX, TXT, NS).
    """
    records = {}
    record_types = ["A", "CNAME", "MX", "TXT", "NS"]
    
    for record_type in record_types:
        try:
            answers = resolver.resolve(subdomain, record_type)
            records[record_type] = [str(rdata) for rdata in answers]
        except (resolver.NoAnswer, resolver.NXDOMAIN, exception.Timeout):
            records[record_type] = []
        except exception.DNSException:
            records[record_type] = []
    
    return records

def main():
    """
    Ana program akışı.
    """
    domain = input("Enter the domain (e.g., youtube.com): ")
    print(f"Scanning subdomains for: {domain}")
    
    # Geçerli ve geçersiz subdomainleri kontrol et
    valid_subdomains, invalid_subdomains = check_subdomain(domain)
    results = {
        "valid_subdomains": [],
        "invalid_subdomains": invalid_subdomains
    }

    for sub in valid_subdomains:
        subdomain_data = {
            "subdomain": sub["subdomain"],
            "ip": sub["ip"],
            "dns_records": get_dns_records(sub["subdomain"]),
        }
        results["valid_subdomains"].append(subdomain_data)
    
    # JSON çıktısını yazdır
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
