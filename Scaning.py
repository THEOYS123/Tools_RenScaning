import os
import time
import sys

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    os.system("cls" if os.name == 'nt' else 'clear')
    print("\033[1;33m███████╗ ██████╗ █████╗ ███╗   ██╗██╗███╗   ██╗ ██████╗")
    print("\033[1;35m██╔════╝██╔════╝██╔══██╗████╗  ██║██║████╗  ██║██╔════╝")
    print("\033[1;36m███████╗██║     ███████║██╔██╗ ██║██║██╔██╗ ██║██║  ███╗")
    print("\033[1;32m╚════██║██║     ██╔══██║██║╚██╗██║██║██║╚██╗██║██║   ██║")
    print("\033[1;34m███████║╚██████╗██║  ██║██║ ╚████║██║██║ ╚████║╚██████╔╝")
    print("\033[1;31m╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝")
    print("\033[1;33m==============================================================")
    print("\033[1;36m         Welcome To Tools Ren Scanning - REN-XPLOIT")
    print("\033[1;37m==============================================================\n")
    
def print_loading():
    loading = ['[          ]', '[=         ]', '[==        ]', '[===       ]', '[====      ]', '[=====     ]', '[======    ]', '[=======   ]', '[========  ]', '[========= ]', '[==========]']
    for frame in loading:
        sys.stdout.write(f"\r\033[1;32m{frame} Loading... Please wait.")
        sys.stdout.flush()
        time.sleep(0.4)
    print("\n")

def main_menu():
    clear()
    print_banner()
    print("\033[1;34m[1] Scanningv1")
    print("\033[1;34m[2] Scanningv2")
    print("\033[1;34m[3] Scanningv3")
    print("\033[1;34m[4] Scanningv4")
    print("\033[1;34m[5] Scanningv5")
    print("\033[1;34m[6] PROXY TOR") 
    print("\033[1;31m[0] Exit")
    print("\033[1;37m")

def get_choice():
    choice = input("\033[1;37m\nEnter your choice: ")
    return choice

def ask_continue():
    while True:
        cont = input("\n\033[1;37mDo you want to return to the main menu? (y/n): ").lower()
        if cont == 'y':
            return True
        elif cont == 'n':
            print("\033[1;31mExiting program...")
            time.sleep(1)
            exit()
        else:
            print("\033[1;31mInvalid input! Please enter 'y' or 'n'.")

def process_choice(choice):
    if choice == '1':
        print("\033[1;32mRunning Scanningv1...")
        print_loading()
        os.system('python ren/cek_web.py')
    elif choice == '2':
        print("\033[1;32mRunning Scanningv2...")
        print_loading()
        os.system('python ren/ScraperHunter.py')
    elif choice == '3':
        print("\033[1;32mRunning Scanningv3...")
        print_loading()
        os.system('python ren/XssHunter.py')
    elif choice == '4':
        print("\033[1;32mRunning Scanningv4...")
        print_loading()
        os.system('python ren/ren-folder1/VulnHunter.py')
    elif choice == '5':
        print("\033[1;32mRunning Scanningv5...")
        print_loading()
        os.system('python ren/cek_header.py')
    elif choice == '6':
        print("\033[1;32mRunning PROXY TOR...")
        print_loading()
        os.system('python proxy.py')
    elif choice == '0':
        print("\033[1;31mExiting program...")
        time.sleep(1)
        exit()
    else:
        print("\033[1;31mInvalid choice! Please select a valid option.")
        time.sleep(2)

if __name__ == "__main__":
    while True:
        main_menu()
        choice = get_choice()
        process_choice(choice)
        if not ask_continue():
            break
