import os
import time

def clear():
    os.system('clear')  # Bersihkan layar terminal

def banner():
    print("\033[1;35m")
    print("                ██╗   ██╗██╗   ██╗██╗     ███╗   ██╗")
    print("                ██║   ██║██║   ██║██║     ████╗  ██║")
    print("                ██║   ██║██║   ██║██║     ██╔██╗ ██║")
    print("                ╚██╗ ██╔╝██║   ██║██║     ██║╚██╗██║")
    print("                ╚████╔╝ ╚██████╔╝███████╗██║ ╚████║")
    print("                 ╚═══╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝")
    print("\033[1;32m")
    print("                 VulnHunter_Ren - Penetration Testing \033[1;37m")
    print("\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[1;37m")
    print("\033[1;33m                      Pilih Tools Untuk Pengujian                    \033[1;37m")
    print("\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[1;37m")
    print(" ╔══════════════════════════════════════════════════════════════════════╗")
    print(" ║    [1] SQL_vuln         - Uji Kerentanannya SQL Injection             ║")
    print(" ║    [2] Xss_Vuln         - Uji Reflected XSS                           ║")
    print(" ║    [3] Parameter Finder - Mancari parameter di seluruh bagian website ║") 
    print(" ║    [4] Keluar           - Keluar dari program                         ║")
    print(" ╚══════════════════════════════════════════════════════════════════════╝")
    print("\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[1;37m")

def menu():
    clear()
    banner()

def pilih_menu():
    choice = input("\033[1;33mPilih nomor (1-3) : \033[1;37m")
    if choice == '1':
        os.system('python ren/ren-folder1/help.py')  
    elif choice == '2':
        os.system('python ren/ren-folder1/txt.py') 
    elif choice == '3':
        os.system('python ren/ren-folder1/scan.py') 
    elif choice == '4':
        print("\033[1;31mKeluar... Terima kasih telah menggunakan VulnHunter_Ren!")
        time.sleep(2)
        exit()
    else:
        print("\033[1;31mPilihan tidak valid! Coba lagi...")
        time.sleep(2)
        pilih_menu()

def animasi_loading():
    loading_text = "\033[1;36mMengatur sistem..."
    for i in range(3):
        print(loading_text + "." * (i + 1))
        time.sleep(0.5)
        clear()
    
    print("\033[1;32mSistem siap, pilih menu!")
    time.sleep(1)

def efek_pilih_menu():
    print("\033[1;34m             >>>>> Selamat datang di tools VulnHunter_Ren>>>>>\033[1;37m")
    time.sleep(1.5)
    print("\033[1;34m>>>>> Menu telah diaktifkan! Silakan pilih opsi yang diinginkan. <<<<<\033[1;37m")

if __name__ == "__main__":
    animasi_loading()
    while True:
        menu()
        efek_pilih_menu()
        pilih_menu()
