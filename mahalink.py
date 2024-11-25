import os
import sys
import time
from colorama import Fore, Style, init
from art import text2art

init(autoreset=True)

mahasiswa_data = {}

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_dots(duration=5, interval=0.5):
    end_time = time.time() + duration
    while time.time() < end_time:
        for i in range(4):
            sys.stdout.write(Fore.WHITE + f'\rSedang Menutup Aplikasi{"." * i}{" " * (3 - i)}')
            sys.stdout.flush()
            time.sleep(interval)
            
def loading_masuk(duration=5, interval=0.5):
    end_time = time.time() + duration
    while time.time() < end_time:
        for i in range(4):
            sys.stdout.write(Fore.WHITE + f'\rTunggu Sebentar{"." * i}{" " * (3 - i)}')
            sys.stdout.flush()
            time.sleep(interval)
    print("\n")

def menu(admin):
    clear_terminal()
    loading_masuk()
    clear_terminal()
    while True:
        print(Fore.BLUE + text2art("MAHALINK", font="block"))
        print(Fore.CYAN + "=" * 40)
        print(Fore.GREEN + "Anda Telah Berhasil Login!")
        print("")
        print(Fore.YELLOW + "=== PILIHAN OPSI YANG TERSEDIA ===") 
        if admin:
            print(Fore.CYAN + "1. Pengumuman Akademik")
            print(Fore.CYAN + "2. Data Kehadiran")
            print(Fore.CYAN + "3. Data Nilai")
            print(Fore.CYAN + "4. Pembayaran UKT")
            print(Fore.CYAN + "5. Keorganisasian")
            print(Fore.CYAN + "6. Dosen Pembimbing")
            print(Fore.CYAN + "7. Status Mahasiswa")
            print(Fore.RED + "8. Keluar")
        else:
            print(Fore.CYAN + "1. Data Kehadiran")
            print(Fore.CYAN + "2. Keorganisasian")
            print(Fore.RED + "3. Keluar")
        print(Fore.CYAN + "=" * 40)
        
        choice = input(Fore.YELLOW + "Pilihlah opsi: ")
        
        if admin:
            if choice == "8":
                print(Fore.GREEN + "Anda telah keluar dari menu.")
                break
            else:
                print(Fore.CYAN + f"Anda memilih opsi {choice}. (Fitur ini belum tersedia)")
        else:
            if choice == "3":
                print(Fore.GREEN + "Anda telah keluar dari menu.")
                break
            else:
                print(Fore.CYAN + f"Anda memilih opsi {choice}. (Fitur ini belum tersedia)")

def register_as_mahasiswa():
    print(Fore.CYAN + "~" * 40)
    print(Fore.BLUE + Style.BRIGHT + "~~~ REGISTRASI MAHASISWA ~~~")
    print(Fore.CYAN + "~" * 40)
    nim = input(Fore.YELLOW + "Masukkan NIM Anda: ")
    password = input(Fore.YELLOW + "Masukkan Password: ")
    if nim.isdigit():
        mahasiswa_data[nim] = password
        print(Fore.GREEN + "Anda Sudah Berhasil Mendaftar, Silakan Login")
    else:
        print(Fore.RED + "NIM harus berupa angka")

def login():
    print(Fore.CYAN + "~" * 40)
    print(Fore.BLUE + Style.BRIGHT + "~~~ LOGIN ~~~")
    print(Fore.CYAN + "~" * 40)
    nama = input(Fore.YELLOW + "Masukkan nama: ")
    password = input(Fore.YELLOW + "Masukkan password: ")

    if nama == "akudosen" and password == "admin555":
        return True
    elif nama in mahasiswa_data and mahasiswa_data[nama] == password:
        return False
    else:
        print(Fore.RED + "Maaf, Username / Password Salah!")
        return None

def main():
    print(Fore.CYAN + "=" * 40)
    print(Fore.BLUE + Style.BRIGHT + "~~~ SELAMAT DATANG ~~~")
    print(Fore.CYAN + "=" * 40)
    while True:
        print(Fore.CYAN + "1. Registrasi Mahasiswa")
        print(Fore.CYAN + "2. Login")
        print(Fore.RED + "3. Keluar")
        choice = input(Fore.YELLOW + "Pilihlah opsi (1/2/3): ")
        
        if choice == '1':
            register_as_mahasiswa()
        elif choice == '2':
            user_type = login()
            if user_type is not None:
                menu(user_type)
        elif choice == '3':
            clear_terminal()
            loading_dots()
            print("")
            print("")
            print(Fore.GREEN + "Terima Kasih Telah Menggunakan Aplikasi MahaLink!")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
