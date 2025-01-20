import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

def crawl_website(base_url):
    visited = set()  # URL yang sudah dikunjungi
    queue = deque([base_url])  # URL yang akan dikunjungi
    matching_urls = []  # URL yang cocok dengan filter

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    while queue:
        current_url = queue.popleft()
        if current_url in visited:
            continue

        print(f"Memeriksa: {current_url}")
        try:
            response = requests.get(current_url, timeout=30, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Gagal mengakses {current_url}: {e}")
            continue

        visited.add(current_url)

        # Parsing halaman HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            parsed_url = urlparse(full_url)

            # Filter domain yang sama
            if parsed_url.netloc == urlparse(base_url).netloc:
                if full_url not in visited and full_url not in queue:
                    queue.append(full_url)

                # Tampilkan URL hanya jika mengandung 'index' atau 'php'
                if 'index' in full_url or 'php' in full_url:
                    if full_url not in matching_urls:
                        matching_urls.append(full_url)

    # Tampilkan hasil
    print("\nHasil URL yang ditemukan:")
    if matching_urls:
        for url in matching_urls:
            print(url)
    else:
        print("Tidak ada URL yang cocok ditemukan.")

# Masukkan URL target
base_url = input("Masukkan URL target (contoh: https://example.com): ").strip()
crawl_website(base_url)
