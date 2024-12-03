import os
import sys
import time
import pandas as pd
from colorama import Fore, Style, init
from art import text2art
from datetime import datetime

init(autoreset=True)

NILAI_FILE = "data_nilai.csv"
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
        
def initialize_kehadiran():
    ATTENDANCE_FILE = "data_kehadiran.csv"
    if not os.path.exists(ATTENDANCE_FILE):
        df = pd.DataFrame(columns=["ID","nim", "matkul", "tanggal", "jam", "status"])
        df.to_csv(ATTENDANCE_FILE, index=False)
    return ATTENDANCE_FILE

def initialize_nilai_file():
    if not os.path.exists(NILAI_FILE):
        df = pd.DataFrame(columns=["ID", "NIM", "Nama", "Mata Kuliah", "Tugas", "UTS", "UAS", "Rata-rata"])
        df.to_csv(NILAI_FILE, index=False)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_dots(duration=1, interval=0.3):
    end_time = time.time() + duration
    while time.time() < end_time:
        for i in range(4):
            sys.stdout.write(Fore.WHITE + f'\rSedang Menutup Aplikasi{"." * i}{" " * (3 - i)}')
            sys.stdout.flush()
            time.sleep(interval)
            
def loading_masuk(duration=1, interval=0.3):
    end_time = time.time() + duration
    while time.time() < end_time:
        for i in range(4):
            sys.stdout.write(Fore.WHITE + f'\rTunggu Sebentar{"." * i}{" " * (3 - i)}')
            sys.stdout.flush()
            time.sleep(interval)
    print("\n")

###  FITUR 1  ###

def display_announcements(file_name):
    initialize_csv(file_name)
    df = pd.read_csv(file_name)
    if df.empty:
        print(Fore.RED + "Belum ada pengumuman.")
    else:
        print(Fore.CYAN + "\nDaftar Pengumuman:")
        print(df.to_markdown(index=False, tablefmt="grid"))

def add_announcement(file_name):
    initialize_csv(file_name)
    judul = input(Fore.YELLOW + "Masukkan judul pengumuman: ")
    isi = input(Fore.YELLOW + "Masukkan isi pengumuman: ")
    tanggal = input(Fore.YELLOW + "Mausukkan tanggal pengumuman: ")
    df = pd.read_csv(file_name)
    new_id = len(df) + 1
    df = pd.concat([df, pd.DataFrame({"ID": [new_id], "Judul": [judul], "Isi": [isi], "Tanggal": [tanggal]})])
    df.to_csv(file_name, index=False)
    print(Fore.GREEN + "Pengumuman berhasil ditambahkan.")

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
                
###  FITUR 2  ###

def initialize_kehadiran():
    ATTENDANCE_FILE = "data_kehadiran.csv"
    if not os.path.exists(ATTENDANCE_FILE):
        df = pd.DataFrame(columns=["ID", "nim", "matkul", "tanggal", "jam", "status"])
        df.to_csv(ATTENDANCE_FILE, index=False)
    return ATTENDANCE_FILE

def admin_manage_kehadiran():
    ATTENDANCE_FILE = initialize_kehadiran()
    df = pd.read_csv(ATTENDANCE_FILE, dtype={"nim": str})

    while True:
        print(Fore.CYAN + "\n=== KELOLA DATA KEHADIRAN ===")
        nim = input(Fore.YELLOW + "Masukkan NIM Mahasiswa yang Dicari: ")
        mahasiswa_data = df[df["nim"] == nim]

        if not mahasiswa_data.empty:
            print(Fore.CYAN + "\nData Kehadiran Mahasiswa:")
            print(mahasiswa_data.to_markdown(index=False, tablefmt="grid"))
            
            print(Fore.YELLOW + "1. Edit Data Kehadiran")
            print(Fore.YELLOW + "2. Kembali")
            choice = input(Fore.YELLOW + "Pilih opsi: ")

            if choice == "1":
                id_to_edit = input(Fore.YELLOW + "Masukkan ID data yang ingin diubah: ")
                if id_to_edit in df["ID"].astype(str).values:
                    index = df[df["ID"] == int(id_to_edit)].index[0]
                    new_status = input(Fore.YELLOW + f"Masukkan status baru (sebelumnya: {df.at[index, 'status']}): ") or df.at[index, "status"]
                    df.at[index, "status"] = new_status.capitalize()
                    df.to_csv(ATTENDANCE_FILE, index=False)
                    clear_terminal()
                    loading_masuk()
                    clear_terminal()
                    print(Fore.GREEN + "Data berhasil diperbarui.")
                    print("")
                    break
                else:
                    print(Fore.RED + "ID tidak ditemukan!")
            elif choice == "2":
                break
            else:
                print(Fore.RED + "Pilihan tidak valid!")
        else:
            print(Fore.RED + "NIM tidak ditemukan.")

def mahasiswa_absensi(nim):
    ATTENDANCE_FILE = initialize_kehadiran()
    df = pd.read_csv(ATTENDANCE_FILE, dtype={"nim": str})

    jadwal_matkul = {
        "Pemrograman Dasar": ("08:00", "09:00"),
        "Matematika Diskrit": ("10:00", "11:00"),
        "Sistem Operasi": ("13:00", "14:00"),
        "Struktur Data": ("16:00", "17:00"),
        "Kecerdasan Buatan": ("20:00", "21:00"),
    }

    print(Fore.CYAN + "\n=== JADWAL MATA KULIAH ===")
    for matkul, (start, end) in jadwal_matkul.items():
        print(Fore.YELLOW + f"- {matkul}: {start} - {end}")

    print(Fore.CYAN + "\n=== ABSENSI ===")
    current_time = datetime.now().strftime("%H:%M")
    print(Fore.GREEN + f"Waktu Sekarang: {current_time}")

    for matkul, (start, end) in jadwal_matkul.items():
        if start <= current_time <= end:
            print(Fore.YELLOW + f"Anda dapat absen untuk mata kuliah {matkul}.")
            absen = input(Fore.YELLOW + f"Absen untuk {matkul} (ya/tidak)? ").strip().lower()
            if absen == "ya":
                new_id = len(df) + 1
                tanggal = input(Fore.YELLOW + f"Masukkan tanggal absensi anda (Tanggal, Nama Bulan, Tahun): ")
                df = pd.concat([df, pd.DataFrame({
                    "ID": [new_id],
                    "nim": [nim],
                    "matkul": [matkul],
                    "tanggal": [tanggal],
                    "jam": [current_time],
                    "status": ["Hadir"]
                })])
                df.to_csv(ATTENDANCE_FILE, index=False)
                print(Fore.GREEN + f"Anda berhasil absen untuk mata kuliah {matkul}.")
        elif current_time < start:
            print(Fore.CYAN + f"Waktu absensi untuk mata kuliah {matkul} belum dimulai.")
        elif current_time > end:
            print(Fore.RED + f"Waktu absensi untuk mata kuliah {matkul} telah berlalu.")

    print(Fore.CYAN + "\nAbsensi selesai.")

def data_kehadiran(role):
    if role == "admin":
        admin_manage_kehadiran()
    elif role == "mahasiswa":
        mahasiswa_absensi(role)
        
###  FITUR 3 ###

def tambah_nilai():
    initialize_nilai_file()
    df = pd.read_csv(NILAI_FILE)

    nim = input(Fore.YELLOW + "Masukkan NIM: ")
    nama = input(Fore.YELLOW + "Masukkan Nama Mahasiswa: ")
    matkul = input(Fore.YELLOW + "Masukkan Mata Kuliah: ")
    tugas = float(input(Fore.YELLOW + "Masukkan Nilai Tugas: "))
    uts = float(input(Fore.YELLOW + "Masukkan Nilai UTS: "))
    uas = float(input(Fore.YELLOW + "Masukkan Nilai UAS: "))

    rata_rata = (tugas + uts + uas) / 3
    new_id = len(df) + 1
    new_data = {
        "ID": new_id,
        "NIM": nim,
        "Nama": nama,
        "Mata Kuliah": matkul,
        "Tugas": tugas,
        "UTS": uts,
        "UAS": uas,
        "Rata-rata": rata_rata
    }
    
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(NILAI_FILE, index=False)

    print(Fore.GREEN + "Data nilai berhasil ditambahkan.")
    print(df.tail(1).to_markdown(index=False))

def lihat_nilai():
    initialize_nilai_file()
    df = pd.read_csv(NILAI_FILE)
    nim = input(Fore.YELLOW + "Masukkan NIM untuk melihat nilai: ").strip()

    # Konversi NIM di database dan input menjadi string yang sama
    data_mahasiswa = df[df["NIM"].astype(str).str.strip() == nim]
    print(Fore.WHITE +df.tail(1).to_markdown(index=False))
    if data_mahasiswa.empty:
        print(Fore.RED + "Data nilai tidak ditemukan.")
        
def edit_nilai():
    initialize_nilai_file()
    df = pd.read_csv(NILAI_FILE)
    lihat_nilai()

    id_nilai = input(Fore.YELLOW + "Masukkan ID nilai yang ingin diubah: ")
    if id_nilai in df["ID"].astype(str).values:
        index = df[df["ID"] == int(id_nilai)].index[0]
        tugas = float(input(Fore.YELLOW + f"Masukkan Nilai Tugas Baru (sebelumnya {df.at[index, 'Tugas']}): ") or df.at[index, "Tugas"])
        uts = float(input(Fore.YELLOW + f"Masukkan Nilai UTS Baru (sebelumnya {df.at[index, 'UTS']}): ") or df.at[index, "UTS"])
        uas = float(input(Fore.YELLOW + f"Masukkan Nilai UAS Baru (sebelumnya {df.at[index, 'UAS']}): ") or df.at[index, "UAS"])

        df.at[index, "Tugas"] = tugas
        df.at[index, "UTS"] = uts
        df.at[index, "UAS"] = uas
        df.at[index, "Rata-rata"] = (tugas + uts + uas) / 3
        df.to_csv(NILAI_FILE, index=False)
        print(Fore.GREEN + "Data nilai berhasil diperbarui.")
    else:
        print(Fore.RED + "ID tidak ditemukan.")

def hapus_nilai():
    initialize_nilai_file()
    df = pd.read_csv(NILAI_FILE)
    lihat_nilai()

    id_nilai = input(Fore.YELLOW + "Masukkan ID nilai yang ingin dihapus: ")
    if id_nilai in df["ID"].astype(str).values:
        df = df[df["ID"] != int(id_nilai)]
        df.to_csv(NILAI_FILE, index=False)
        print(Fore.GREEN + "Data nilai berhasil dihapus.")
    else:
        print(Fore.RED + "ID tidak ditemukan.")

def data_nilai(role, nim):
    if role == "admin":
        while True:
            print(Fore.CYAN + "\n=== MANAJEMEN DATA NILAI ===")
            print(Fore.CYAN +"1. Tambah Nilai Mahasiswa")
            print(Fore.CYAN +"2. Lihat Nilai Mahasiswa")
            print(Fore.CYAN +"3. Edit Nilai Mahasiswa")
            print(Fore.CYAN +"4. Hapus Nilai Mahasiswa")
            print(Fore.RED + "5. Kembali")
            pilihan = input(Fore.YELLOW + "Pilih opsi: ")

            if pilihan == "1":
                tambah_nilai()
            elif pilihan == "2":
                lihat_nilai()
            elif pilihan == "3":
                edit_nilai()
            elif pilihan == "4":
                hapus_nilai()
            elif pilihan == "5":
                break
            else:
                print(Fore.RED + "Pilihan tidak valid.")
    elif role == "mahasiswa":
        print(Fore.CYAN + "\n=== DATA NILAI MAHASISWA ===")
        lihat_nilai()

def menu(role, nim):
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
        
        choice = input(Fore.YELLOW + "Pilih opsi: ").strip()
        
        if role == "admin":
            if choice == "1":
                pengumuman_akademik(role)
            elif choice == "2":
                data_kehadiran(role)
            elif choice == "3":
                data_nilai(role,nim)
            elif choice == "8":
                print(Fore.GREEN + "Anda telah keluar dari menu.")
                break
            else:
                print(Fore.CYAN + f"Anda memilih opsi {choice}. (Fitur ini belum tersedia)")
        elif role == "mahasiswa":
            if choice == "1":
                pengumuman_akademik(role)
            elif choice == "2":
                mahasiswa_absensi(nim)
            elif choice == "3":
                data_nilai(role,nim)
            elif choice == "8":
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
            return stored_role, nim
        else:
            print(Fore.RED + "Password salah!")
    else:
        print(Fore.RED + "NIM tidak ditemukan!")
    return None, None

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
            user_role, user_nim = login()
            if user_role:
                menu(user_role, user_nim)
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
