# Domain ve Web Güvenliği Analiz Aracı

Bu proje, bir domainin WHOIS bilgilerini, DNS kayıtlarını, subdomainlerini, HTTP güvenlik başlıklarını ve sosyal medya varlıklarını analiz eden bir araçtır. Her hafta farklı bir modül eklenerek proje genişletilmiştir.

## Özellikler
- **WHOIS Sorgusu:** Domainin kayıt bilgilerini (oluşturulma tarihi, sona erme tarihi, kayıt şirketi vb.) getirir.
- **DNS Kayıtları:** A, AAAA, MX, NS, CNAME ve TXT kayıtlarını kontrol eder.
- **Subdomain Tarama:** Geçerli ve geçersiz subdomainleri tespit eder.
- **HTTP Güvenlik Başlıkları:** HSTS, CSP, X-Frame-Options gibi güvenlik başlıklarını analiz eder.
- **Sosyal Medya Analizi:** Twitter ve LinkedIn üzerinden şirket bilgilerini toplar.

## Kurulum
1. Python 3.x'in yüklü olduğundan emin olun.
2. Gerekli kütüphaneleri yükleyin:
   ```bash
  pip install -r requirements.txt

##Projeyi Çalıştırın
python hafta1.py  # WHOIS ve DNS sorgusu için
python hafta2.py  # Subdomain tarama için
python hafta3.py  # API ile domain ve IP bilgileri için
python hafta4.py  # Sosyal medya verileri için
python hafta5.py  # HTTP başlıkları analizi için
