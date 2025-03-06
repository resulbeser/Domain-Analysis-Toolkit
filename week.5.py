import requests
import json

def analyze_http_headers(url):
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        security_headers = {
            "Strict-Transport-Security": "HSTS (HTTP Strict Transport Security) kullanımı",
            "Content-Security-Policy": "İçerik Güvenlik Politikası (CSP) kullanımı",
            "X-Frame-Options": "Clickjacking saldırılarını önleme",
            "X-Content-Type-Options": "MIME türü sahtekarlığını önleme",
            "Referrer-Policy": "Referrer bilgisi kontrolü",
            "Permissions-Policy": "Tarayıcı izinlerini sınırlama"
        }

        security_results = {}
        for header, description in security_headers.items():
            security_results[header] = {
                "value": headers.get(header, "Eksik"),
                "description": description
            }

        result = {
            "url": url,
            "http_headers": dict(headers),
            "security_analysis": security_results
        }

        # JSON olarak ekrana yazdır
        print(json.dumps(result, indent=4, ensure_ascii=False))

        # JSON'u dosyaya kaydet
        with open("cıktı.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": str(e)}, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    site = input("Analiz edilecek web sitesi (https://example.com): ").strip()
    if not site.startswith("http"):
        site = "https://" + site  # HTTP veya HTTPS eklenmemişse otomatik olarak HTTPS ekleyelim
    analyze_http_headers(site)
   

