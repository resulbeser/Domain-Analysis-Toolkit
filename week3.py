import requests
import json

# API Anahtarını buraya ekleyin (Geçerli olup olmadığını kontrol edin)
api_key = "ENTER API KEY"

# Kullanıcıdan domain girişini al
domain = input("Domain ismini girin (örn: example.org): ")

# API URL'leri
url = f"https://api.securitytrails.com/v1/domain/{domain}"
associated_url = f"https://api.securitytrails.com/v1/associated/{domain}"

headers = {"APIKEY": api_key}

# SecurityTrails API çağrıları
response = requests.get(url, headers=headers)
associated_response = requests.get(associated_url, headers=headers)

output = {"domain": domain, "ip_info": [], "associated_domains": []}

if response.status_code == 200:
    data = response.json()

    if 'current_dns' in data:
        # A (IPv4) ve AAAA (IPv6) kayıtlarını al
        ipv4_addresses = [
            entry["ip"] for entry in data["current_dns"].get("a", {}).get("values", [])
        ]
        ipv6_addresses = [
            entry["ipv6"] for entry in data["current_dns"].get("aaaa", {}).get("values", [])
        ]

        # IPInfo API'den bilgi çekme
        def get_ip_info(ip, ip_type):
            try:
                ip_info = requests.get(f"https://ipinfo.io/{ip}/json").json()
                return {
                    "ip": ip,
                    "type": ip_type,
                    "location": {
                        "city": ip_info.get("city"),
                        "region": ip_info.get("region"),
                        "country": ip_info.get("country"),
                        "coordinates": ip_info.get("loc"),
                    },
                    "organization": ip_info.get("org"),
                }
            except Exception as e:
                return {"ip": ip, "error": str(e)}

        # IPv4 & IPv6 bilgilerini al ve listeye ekle
        for ip in ipv4_addresses:
            output["ip_info"].append(get_ip_info(ip, "IPv4"))
        for ipv6 in ipv6_addresses:
            output["ip_info"].append(get_ip_info(ipv6, "IPv6"))

else:
    print(f"Hata: SecurityTrails API isteği başarısız oldu. Status Code: {response.status_code}")

# Firma ile ilişkili diğer domainleri al (Enterprise API gerektiriyor)
if associated_response.status_code == 200:
    associated_data = associated_response.json()
    if "domains" in associated_data:
        output["associated_domains"] = associated_data["domains"]
    else:
        print("Uyarı: İlgili domainler alınamadı. API Enterprise sürüm gerektirebilir.")

print(json.dumps(output, indent=4))
