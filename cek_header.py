import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from termcolor import colored  # buat warna teks

# Fungsi untuk validasi nomor telepon internasional (E.164 format)
def is_valid_phone_number(number):
    # Format internasional: +[kode negara][nomor telepon]
    pattern = re.compile(r"^\+?[1-9]\d{1,14}$")  # Regex untuk format E.164
    return bool(pattern.match(number))

def analyze_url(url):
    print(f"Analyzing {url}...\n")

    # HTTP Headers
    headers = requests.get(url).headers
    print("HTTP Headers:")
    for key, value in headers.items():
        print(f"{key}: {value}")

    # Fitur tambahan - SSL/TLS Certificate Check
    try:
        response = requests.get(url, timeout=5)
        ssl_certificate = response.raw._connection.sock.getpeercert()
        print("\nSSL/TLS Certificate Info:")
        print(ssl_certificate)
    except Exception as e:
        print("\nSSL/TLS Certificate Check: Failed")
        print(f"Error: {e}")

    # Fitur tambahan - Cek Robots.txt
    robots_url = urlparse(url)._replace(path='/robots.txt').geturl()
    try:
        robots = requests.get(robots_url)
        if robots.status_code == 200:
            print("\nRobots.txt found:")
            print(robots.text)
        else:
            print("\nRobots.txt not found.")
    except requests.exceptions.RequestException:
        print("\nError fetching robots.txt")

    # Fitur tambahan - Cek Meta SEO Tags
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        meta_tags = soup.find_all('meta')
        print("\nMeta Tags SEO:")
        for tag in meta_tags:
            if tag.get('name') or tag.get('property'):
                print(f"{tag.get('name') or tag.get('property')}: {tag.get('content')}")
    except Exception as e:
        print("\nError fetching Meta SEO Tags:")
        print(f"Error: {e}")

    # SQL Injection Check
    payload = "' OR 1=1 --"
    print(f"\nChecking for SQL Injection vulnerability on {url + payload}...")
    try:
        response = requests.get(url + payload)
        if "error" in response.text.lower() or "mysql" in response.text.lower():
            print(colored("\nPossible SQL Injection vulnerability detected!", "blue"))
        else:
            print("\nNo SQL Injection vulnerability found.")
    except requests.exceptions.RequestException as e:
        print("\nError with request:")
        print(f"Error: {e}")

    # Security Headers Check
    security_headers = [
        ("X-Content-Type-Options", "nosniff"),
        ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
        ("X-XSS-Protection", "1; mode=block"),
        ("Content-Security-Policy", "default-src 'self'"),
        ("Referrer-Policy", "no-referrer-when-downgrade"),
        ("X-Frame-Options", "SAMEORIGIN")
    ]

    print("\nSecurity Headers Check:")
    for header, expected_value in security_headers:
        if headers.get(header) != expected_value:
            print(colored(f"Warning: {header} is missing or not configured properly!", "blue"))

    # HSTS Check
    if "Strict-Transport-Security" not in headers:
        print(colored("\nWarning: HSTS not enabled! (Sensitive data can be intercepted over HTTP)", "blue"))

    # Content-Type Check
    if "Content-Type" in headers and "text/html" in headers["Content-Type"]:
        print(colored("\nWarning: Content-Type header is set to 'text/html' which might indicate outdated configuration.", "blue"))

    # Cari nomor telepon yang valid
    print("\nChecking for valid phone numbers on the page...\n")
    phone_numbers = set()  # Gunakan set supaya nomor yang sama tidak muncul dua kali

    # Mengambil konten dari halaman dan mencari nomor telepon
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text_content = soup.get_text()

    # Cari nomor telepon dengan pola yang sesuai
    potential_numbers = re.findall(r"(\+?\d[\d\- ]{7,15})", text_content)

    # Validasi nomor telepon yang ditemukan
    valid_numbers = [num for num in potential_numbers if is_valid_phone_number(num)]

    if valid_numbers:
        print(colored("Valid Phone Numbers found:", "green"))
        for num in valid_numbers:
            print(f"Valid: {num}")
    else:
        print("No valid phone numbers found.")

if __name__ == "__main__":
    url = input("Enter URL to analyze: ")
    analyze_url(url)
