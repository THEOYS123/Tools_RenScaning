from bs4 import BeautifulSoup
import urllib.parse
from termcolor import colored
from colorama import init, Fore, Style
import time
import random
import requests
import os

# Inisialisasi Colorama
init()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
]

SENSITIVE_KEYWORDS = [
 "informasi pemerintah", "data instansi pemerintah"
]

default_queries1 = [
    "filetype:pdf biodata AND organization",
    "filetype:xls biodata AND organization",
    "intitle:index.of inurl:pegawai ext:pdf OR ext:xls OR ext:doc",
]

default_queries2 = [
 "inurl:rubp.php?idr=", "inurl:offer.php?idf=", "inurl:art.php?idm=", "inurl:title.php?="
  ]

def google_search(query, num_results=50, delay=3, recent=True):
    query = urllib.parse.quote_plus(query)
    results = []
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    start = 0

    while len(results) < num_results:
        url = f"https://www.google.com/search?q={query}&num=10&start={start}"
        if recent:
            url += "&tbs=qdr:y"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for g in soup.find_all('div', class_='tF2Cxc'):
                link_tag = g.find('a')
                title_tag = g.find('h3')
                desc_tag = g.find('div', class_='IsZvec')
                if link_tag and title_tag:
                    link = link_tag['href']
                    title = title_tag.text
                    description = desc_tag.text.strip() if desc_tag else "No description"

                    # Hindari duplikasi
                    if not any(result['link'] == link for result in results):
                        results.append({'title': title, 'link': link, 'description': description})

            # Periksa apakah kita telah mencapai jumlah hasil yang diinginkan
            if len(results) >= num_results:
                break

            # Jika tidak ada hasil baru, hentikan pencarian
            if not soup.find_all('div', class_='tF2Cxc'):
                print(colored("Tidak ada hasil tambahan yang ditemukan.", "yellow"))
                break

            # Tambahkan delay untuk menghindari pemblokiran
            time.sleep(random.uniform(delay, delay + 2))

        except Exception as e:
            print(colored(f"Error fetching data for query '{query}': {e}", "red"))
            break

        start += 10  # Pindah ke halaman berikutnya

    return random.sample(results, min(len(results), num_results))  # Acak hasilnya

def main_menu():
    os.system('clear')
    logo = r"""
 SCRIPT SCRAPER by ＲＥＮ-ＸＰＬＯＩＴ Ｘ ＤＫＳ
                                               """
    print(colored(logo, 'white', 'on_red'))

    while True:
        print("\nMenu:")
        print("1. Scrape Google Results dengan Query Default (Scaner Website Pemerintah)")
        print("2. Scrape Google Results dengan Query Default (Scaner Website Vuln)")
        print("3. Masukkan Query Custom untuk Scraping (Dengan Filter)")
        print("4. Exit")

        choice = input("Pilih menu (1/2/3/4): ")

        if choice == "1":
            try:
                max_results = int(input("Masukkan jumlah hasil maksimal per query (contoh: 10): "))
                if max_results <= 0:
                    raise ValueError("Jumlah hasil harus lebih besar dari 0.")
            except ValueError as e:
                print(colored(f"Input tidak valid: {e}. Menggunakan default 10 hasil.", "yellow"))
                max_results = 10

            run_scraper(default_queries1, max_results=max_results)
        elif choice == "2":
            try:
                max_results = int(input("Masukkan jumlah hasil maksimal per query (contoh: 10): "))
                if max_results <= 0:
                    raise ValueError("Jumlah hasil harus lebih besar dari 0.")
            except ValueError as e:
                print(colored(f"Input tidak valid: {e}. Menggunakan default 10 hasil.", "yellow"))
                max_results = 10

            run_scraper(default_queries2, max_results=max_results)
        elif choice == "3":
            custom_query = input("Masukkan query custom (pisahkan dengan koma untuk banyak query): ")
            queries = [q.strip() for q in custom_query.split(',')]

            try:
                max_results = int(input("Masukkan jumlah hasil maksimal per query (contoh: 10): "))
                if max_results <= 0:
                    raise ValueError("Jumlah hasil harus lebih besar dari 0.")
            except ValueError as e:
                print(colored(f"Input tidak valid: {e}. Menggunakan default 10 hasil.", "yellow"))
                max_results = 10

            filter_keyword = input("Masukkan keyword filter untuk hasil (kosongkan jika tidak ingin filter): ").lower()

            run_scraper(queries, max_results, filter_keyword)
        elif choice == "4":
            print(colored("Exiting program. Thank you for using REN-SCRAPER!", "green"))
            break
        else:
            print(colored("Pilihan tidak valid. Coba lagi.", "red"))
            
def run_scraper(queries, max_results=10, filter_keyword=""):
    all_results = []
    seen_links = set()

    for query in queries:
        print(colored(f"Searching for: {query}", "cyan"))
        results = google_search(query, num_results=max_results)
        for result in results:
            if result['link'] not in seen_links:
                if not filter_keyword or filter_keyword in result['title'].lower() or filter_keyword in result['description'].lower():
                    all_results.append(result)
                    seen_links.add(result['link'])

    if all_results:
        for idx, result in enumerate(all_results, start=1):
            link_color = Fore.RED if idx % 2 == 0 else Fore.WHITE
            print(f"{idx}. {result['title']}\n   {link_color}{result['link']}{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}Description: {result['description']}{Style.RESET_ALL}\n")

        save_choice = input(colored("Do you want to save the results? (y/n): ", "cyan")).lower()
        if save_choice == 'y':
            save_results_to_file(all_results)
        else:
            print(colored("Results not saved. Thank you for using REN-SCRAPER!", "yellow"))
    else:
        print(colored("No results found.", "red"))

def save_results_to_file(results, file_path="/sdcard/scraped_results.txt"):
    try:
        with open(file_path, 'a') as file:
            for result in results:
                file.write(f"Title: {result['title']}\n")
                file.write(f"Link: {result['link']}\n")
                file.write(f"Description: {result['description']}\n\n")
        print(colored(f"Results saved to {file_path}", "green"))
    except Exception as e:
        print(colored(f"Error saving results: {e}", "red"))

if __name__ == "__main__":
    main_menu()
