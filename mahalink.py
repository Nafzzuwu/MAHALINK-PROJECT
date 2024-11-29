import os
import sys
import time
import pandas as pd
from colorama import Fore, Style, init
from art import text2art

init(autoreset=True)

CSV_FILE = "mahasiswa_data.csv"
LOMBA_FILE = "pengumuman_lomba.csv"
LIBUR_FILE = "pengumuman_libur.csv"

if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["nim", "password", "role"])
    df.to_csv(CSV_FILE, index=False)

df = pd.read_csv(CSV_FILE, dtype={"nim": str})
if "4646" not in df["nim"].values:
    admin_data = pd.DataFrame({"nim": ["4646"], "password": ["akudosen"], "role": ["admin"]})
    admin_data.to_csv(CSV_FILE, mode='a', header=False, index=False)

def initialize_csv(file_name):
    if not os.path.exists(file_name):
        df = pd.DataFrame(columns=["ID", "Judul", "Isi", "Tanggal"])
        df.to_csv(file_name, index=False)

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

# Tampilkan semua pengumuman dari file CSV
def display_announcements(file_name):
    initialize_csv(file_name)
    df = pd.read_csv(file_name)
    if df.empty:
        print(Fore.RED + "Belum ada pengumuman.")
    else:
        print(Fore.CYAN + "\nDaftar Pengumuman:")
        print(df.to_markdown(index=False, tablefmt="grid"))

# Tambah pengumuman baru
def add_announcement(file_name):
    initialize_csv(file_name)
    judul = input(Fore.YELLOW + "Masukkan judul pengumuman: ")
    isi = input(Fore.YELLOW + "Masukkan isi pengumuman: ")
    tanggal = input(Fore.YELLOW + "Mausukkan tanggal pengumuman (YYYY-MM-DD): ")
    df = pd.read_csv(file_name)
    new_id = len(df) + 1
    df = pd.concat([df, pd.DataFrame({"ID": [new_id], "Judul": [judul], "Isi": [isi], "Tanggal": [tanggal]})])
    df.to_csv(file_name, index=False)
    print(Fore.GREEN + "Pengumuman berhasil ditambahkan.")

# Edit pengumuman berdasarkan ID
def edit_announcement(file_name):
    initialize_csv(file_name)
    display_announcements(file_name)
    id_to_edit = input(Fore.YELLOW + "Masukkan ID pengumuman yang ingin diubah: ")
    df = pd.read_csv(file_name)
    if id_to_edit in df["ID"].astype(str).values:
        index = df[df["ID"] == int(id_to_edit)].index[0]
        judul = input(Fore.YELLOW + f"Masukkan judul baru (sebelumnya: {df.at[index, 'Judul']}): ") or df.at[index, "Judul"]
        isi = input(Fore.YELLOW + f"Masukkan isi baru (sebelumnya: {df.at[index, 'Isi']}): ") or df.at[index, "Isi"]
        df.at[index, "Judul"] = judul
        df.at[index, "Isi"] = isi
        df.to_csv(file_name, index=False)
        print(Fore.GREEN + "Pengumuman berhasil diubah.")
    else:
        print(Fore.RED + "ID tidak ditemukan.")

# Hapus pengumuman berdasarkan ID
def delete_announcement(file_name):
    initialize_csv(file_name)
    display_announcements(file_name)
    id_to_delete = input(Fore.YELLOW + "Masukkan ID pengumuman yang ingin dihapus: ")
    df = pd.read_csv(file_name)
    if id_to_delete in df["ID"].astype(str).values:
        df = df[df["ID"] != int(id_to_delete)]
        df.to_csv(file_name, index=False)
        print(Fore.GREEN + "Pengumuman berhasil dihapus.")
    else:
        print(Fore.RED + "ID tidak ditemukan.")

# Fitur Pengumuman Akademik berdasarkan role
def pengumuman_akademik(role):
    if role == "admin":
        while True:
            print(Fore.CYAN + "\n=== PENGUMUMAN AKADEMIK (ADMIN) ===")
            print(Fore.CYAN + "1. Tambah Pengumuman Lomba")
            print(Fore.CYAN + "2. Tambah Pengumuman Libur")
            print(Fore.CYAN + "3. Lihat Semua Pengumuman Lomba")
            print(Fore.CYAN + "4. Lihat Semua Pengumuman Libur")
            print(Fore.CYAN + "5. Edit Pengumuman Lomba")
            print(Fore.CYAN + "6. Edit Pengumuman Libur")
            print(Fore.CYAN + "7. Hapus Pengumuman Lomba")
            print(Fore.CYAN + "8. Hapus Pengumuman Libur")
            print(Fore.RED + "9. Kembali ke Menu Utama")
            choice = input(Fore.YELLOW + "Pilih opsi: ")

            if choice == "1":
                add_announcement(LOMBA_FILE)
            elif choice == "2":
                add_announcement(LIBUR_FILE)
            elif choice == "3":
                display_announcements(LOMBA_FILE)
            elif choice == "4":
                display_announcements(LIBUR_FILE)
            elif choice == "5":
                edit_announcement(LOMBA_FILE)
            elif choice == "6":
                edit_announcement(LIBUR_FILE)
            elif choice == "7":
                delete_announcement(LOMBA_FILE)
            elif choice == "8":
                delete_announcement(LIBUR_FILE)
            elif choice == "9":
                break
            else:
                print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")
    elif role == "mahasiswa":
        while True:
            print(Fore.CYAN + "\n=== PENGUMUMAN AKADEMIK (MAHASISWA) ===")
            print(Fore.CYAN + "1. Lihat Pengumuman Lomba")
            print(Fore.CYAN + "2. Lihat Pengumuman Libur")
            print(Fore.RED + "3. Kembali ke Menu Utama")
            choice = input(Fore.YELLOW + "Pilih opsi: ")

            if choice == "1":
                display_announcements(LOMBA_FILE)
            elif choice == "2":
                display_announcements(LIBUR_FILE)
            elif choice == "3":
                break
            else:
                print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")

def menu(role):
    clear_terminal()
    loading_masuk()
    clear_terminal()
    print(Fore.BLUE + text2art("MAHALINK", font="block"))
    print(Fore.CYAN + "=" * 40)
    print(Fore.GREEN + f"Anda Telah Berhasil Login Sebagai {role.capitalize()}!")
    while True:
        print(Fore.YELLOW + "=== PILIHAN OPSI YANG TERSEDIA ===")
        if role == "admin":
            print(Fore.CYAN + "1. Pengumuman Akademik")
            print(Fore.CYAN + "2. Data Kehadiran")
            print(Fore.CYAN + "3. Data Nilai")
            print(Fore.CYAN + "4. Pembayaran UKT")
            print(Fore.CYAN + "5. Keorganisasian")
            print(Fore.CYAN + "6. Dosen Pembimbing")
            print(Fore.CYAN + "7. Status Mahasiswa")
            print(Fore.RED + "8. Keluar")
        elif role == "mahasiswa":
            print(Fore.CYAN + "1. Pengumuman Akademik")
            print(Fore.CYAN + "2. Data Kehadiran")
            print(Fore.CYAN + "3. Data Nilai")
            print(Fore.CYAN + "4. Pembayaran UKT")
            print(Fore.CYAN + "5. Keorganisasian")
            print(Fore.CYAN + "6. Dosen Pembimbing")
            print(Fore.CYAN + "7. Status Mahasiswa")
            print(Fore.RED + "8. Keluar")
        print(Fore.CYAN + "=" * 40)
        
        choice = input(Fore.YELLOW + "Pilihlah opsi: ")
        
        if role == "admin":
            if choice == "1":
                pengumuman_akademik(role)
            if choice == "8":
                print(Fore.GREEN + "Anda telah keluar dari menu.")
                break
            else:
                print(Fore.CYAN + f"Anda memilih opsi {choice}. (Fitur ini belum tersedia)")
        elif role == "mahasiswa":
            if choice == "1":
                pengumuman_akademik(role)
            if choice == "8":
                print(Fore.GREEN + "Anda telah keluar dari menu.")
                break
            else:
                print(Fore.CYAN + f"Anda memilih opsi {choice}. (Fitur ini belum tersedia)")

def register_as_mahasiswa():
    print(Fore.CYAN + "~" * 40)
    print(Fore.BLUE + Style.BRIGHT + "~~~ REGISTRASI ~~~")
    print(Fore.CYAN + "~" * 40)
    nim = input(Fore.YELLOW + "Masukkan NIM Anda: ")
    password = input(Fore.YELLOW + "Masukkan Password: ")
    
    if nim.isdigit():
        df = pd.read_csv(CSV_FILE, dtype={"nim": str})
        
        if nim in df["nim"].values:
            print(Fore.RED + "NIM sudah terdaftar! Silakan gunakan NIM lain.")
        else:
            role = "admin" if nim == "4646" else "mahasiswa"
            new_data = pd.DataFrame({"nim": [nim], "password": [password], "role": [role]})
            new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
            print(Fore.GREEN + f"Anda Sudah Berhasil Mendaftar Sebagai {role.capitalize()}, Silakan Login.")
    else:
        print(Fore.RED + "NIM harus berupa angka!")

def login():
    print(Fore.CYAN + "~" * 40)
    print(Fore.BLUE + Style.BRIGHT + "~~~ LOGIN ~~~")
    print(Fore.CYAN + "~" * 40)
    nim = input(Fore.YELLOW + "Masukkan NIM Anda: ")
    password = input(Fore.YELLOW + "Masukkan password: ")

    df = pd.read_csv(CSV_FILE, dtype={"nim": str})
    
    if nim in df["nim"].values:
        stored_password = df.loc[df["nim"] == nim, "password"].values[0]
        stored_role = df.loc[df["nim"] == nim, "role"].values[0]
        if stored_password == password:
            return stored_role
        else:
            print(Fore.RED + "Password salah!")
    else:
        print(Fore.RED + "NIM tidak ditemukan!")
    return None

def main():
    print(Fore.CYAN + "=" * 40)
    print(Fore.BLUE + Style.BRIGHT + "~~~ SELAMAT DATANG ~~~")
    print(Fore.CYAN + "=" * 40)
    while True:
        print(Fore.CYAN + "1. Registrasi")
        print(Fore.CYAN + "2. Login")
        print(Fore.RED + "3. Keluar")
        choice = input(Fore.YELLOW + "Pilihlah opsi (1/2/3): ")
        
        if choice == '1':
            register_as_mahasiswa()
        elif choice == '2':
            user_role = login()
            if user_role:
                menu(user_role)
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
