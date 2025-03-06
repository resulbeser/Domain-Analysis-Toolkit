import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import chromedriver_autoinstaller

# ChromeDriver'ı otomatik yükleme
chromedriver_autoinstaller.install()

# Selenium için tarayıcı başlatma fonksiyonu
def start_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran aç
    driver = webdriver.Chrome(service=Service(), options=options)
    return driver

# Twitter Verisi Çekme (Selenium Kullanarak)
def get_twitter_data(username):
    driver = start_browser()
    url = f'https://twitter.com/{username}'
    driver.get(url)
    time.sleep(5)  # Sayfanın yüklenmesini bekle

    try:
        bio = driver.find_element(By.XPATH, '//div[@data-testid="UserDescription"]').text
    except:
        bio = "Bio bulunamadı"

    try:
        name = driver.find_element(By.XPATH, '//div[@data-testid="UserName"]').text
    except:
        name = "İsim bulunamadı"

    driver.quit()

    return {
        "name": name,
        "bio": bio,
        "twitter_handle": username
    }

# LinkedIn Çalışan Verilerini Çekme
def get_linkedin_employees(company_url):
    driver = start_browser()
    
    # LinkedIn giriş işlemleri
    driver.get("https://www.linkedin.com/login")
    input("Lütfen giriş yapın ve ENTER'a basın...")  # Manuel giriş yapılması için bekler

    driver.get(company_url)

    time.sleep(5)  # Sayfanın yüklenmesini bekle
    employees = driver.find_elements(By.CSS_SELECTOR, ".org-people-profile-card__profile-title")
    positions = driver.find_elements(By.CSS_SELECTOR, ".org-people-profile-card__headline")

    employee_data = []
    for emp, pos in zip(employees, positions):
        employee_data.append({
            "name": emp.text,
            "position": pos.text
        })

    driver.quit()
    return employee_data

# Ana Fonksiyon
def main():
    company_name = input("Şirket ismini girin: ")

    # Twitter verisini al
    twitter_username = input(f"{company_name} için Twitter kullanıcı adını girin: ")
    twitter_data = get_twitter_data(twitter_username)
    
    # LinkedIn verisini al
    company_linkedin_url = f"https://www.linkedin.com/company/{company_name}/people/"
    linkedin_employees = get_linkedin_employees(company_linkedin_url)

    # Verileri JSON'a kaydetme
    data = {
        "company_name": company_name,
        "twitter_data": twitter_data,
        "linkedin_employees": linkedin_employees
    }

    with open(f'{company_name}_social_media_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"{company_name} hakkında veriler başarıyla kaydedildi.")

if __name__ == "__main__":
    main()

# JSON Verisini Analiz Etme
def analyze_data(json_filename):
    with open(json_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    company_name = data["company_name"]
    twitter_data = data["twitter_data"]
    linkedin_employees = data["linkedin_employees"]

    report = f"📌 {company_name} Sosyal Medya ve Çalışan Analizi\n"
    report += "=" * 50 + "\n\n"

    report += "🔹 **Twitter Bilgileri**\n"
    report += f"   - Kullanıcı Adı: {twitter_data.get('name', 'Bilinmiyor')}\n"
    report += f"   - Biyografi: {twitter_data.get('bio', 'Bilinmiyor')}\n"
    report += f"   - Twitter Kullanıcı Adı: @{twitter_data.get('twitter_handle', 'Bilinmiyor')}\n\n"

    report += "🔹 **LinkedIn Çalışanları**\n"
    for employee in linkedin_employees:
        report += f"   - {employee['name']} | {employee['position']}\n"
    report += f"   - Toplam Çalışan Sayısı: {len(linkedin_employees)}\n\n"

    report_filename = f"{company_name}_analysis_report.txt"
    with open(report_filename, "w", encoding="utf-8") as report_file:
        report_file.write(report)

    print(f"📄 Rapor oluşturuldu: {report_filename}")

# Ana kod bloğunun sonuna ekle
company_name = input("Şirket ismini gir (JSON dosya adı olmadan yaz): ")
analyze_data(f"{company_name}_social_media_data.json")
