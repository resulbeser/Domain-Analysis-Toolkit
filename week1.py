import whois
import dns.resolver
import json

def domain_bilgisi(x):
    try:
        # WHOIS sorgusu
        w = whois.whois(x)
        whois_data = {
            "domain": w.domain_name,
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "whois_server": w.whois_server,
        }
        return {"success": True, "whois_data": whois_data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def dns_kayitlari(domain_name):
    kayit_turleri = ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT']
    dns_results = {}

    for kayit_turu in kayit_turleri:
        try:
            cevap = dns.resolver.resolve(domain_name, kayit_turu)
            dns_results[kayit_turu] = [rdata.to_text() for rdata in cevap]
        except dns.resolver.NoAnswer:
            dns_results[kayit_turu] = None  # Kayıt bulunamadı
        except dns.resolver.NXDOMAIN:
            return {"success": False, "error": f"{domain_name} alan adı bulunamadı."}
        except Exception as e:
            dns_results[kayit_turu] = f"Hata: {str(e)}"

    return {"success": True, "dns_data": dns_results}

if __name__ == "__main__":
    domain = input("Sorgulanacak domain adını girin: ").strip()

    if not domain:
        print("Lütfen geçerli bir domain adı girin.")
    else:
        # WHOIS ve DNS kayıtlarını al
        whois_result = domain_bilgisi(domain)
        dns_result = dns_kayitlari(domain)

        # Sonuçları birleştir
        final_result = {
            "domain": domain,
            "whois_result": whois_result,
            "dns_result": dns_result,
        }

        # JSON formatında çıktı
        try:
            print(json.dumps(final_result, indent=4, ensure_ascii=False))
        except Exception as e:
            print(f"Sonuçlar JSON formatına dönüştürülürken hata oluştu: {str(e)}")
