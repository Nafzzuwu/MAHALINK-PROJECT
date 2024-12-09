import os
import sys
import time
import pandas as pd
from colorama import Fore, Style, init
from art import text2art
from datetime import datetime

init(autoreset=True)

KEHADIRAN_FILE = "data_kehadiran.csv"
NILAI_FILE = "data_nilai.csv"
CSV_FILE = "mahasiswa_data.csv"
LOMBA_FILE = "pengumuman_lomba.csv"
LIBUR_FILE = "pengumuman_libur.csv"
UKT_FILE = "data_ukt.csv"
UKM_FILE = "data_ukm.csv"
DOSPEM_FILE = "data_dosen_pembimbing.csv"
STATUS_FILE = "data_status.csv"

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
    if not os.path.exists(KEHADIRAN_FILE):
        df = pd.DataFrame(columns=["ID","nim", "matkul", "tanggal", "jam", "status"])
        df.to_csv(KEHADIRAN_FILE, index=False)
    return KEHADIRAN_FILE

def initialize_nilai_file():
    if not os.path.exists(NILAI_FILE):
        df = pd.DataFrame(columns=["ID", "NIM", "Nama", "Mata Kuliah", "Tugas", "UTS", "UAS", "Rata-rata"])
        df.to_csv(NILAI_FILE, index=False)
        
def initialize_ukt_file():
    if not os.path.exists(UKT_FILE):
        df = pd.DataFrame(columns=["NIM", "NAMA", "NOMINAL", "STATUS"])
        df.to_csv(UKT_FILE, index=False)
        
def initialize_ukm_file():
    if not os.path.exists(UKM_FILE):
        df = pd.DataFrame(columns=["Nama UKM", "Status Perekrutan", "Informasi Lanjut"])
        df.to_csv(UKM_FILE, index=False)
        
def initialize_dospem_file():
    if not os.path.exists(DOSPEM_FILE):
        df = pd.DataFrame(columns=["ID", "NIM", "Nama", "Dospem", "Penelitian"])
        df.to_csv(DOSPEM_FILE, index=False)

def initialize_status_file():
    if not os.path.exists(STATUS_FILE):
        df = pd.DataFrame(columns=["NIM", "Nama", "Angkatan", "Status Kelulusan", "Prestasi"])
        df.to_csv(STATUS_FILE, index=False)
        
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
        print(Fore.CYAN + "\n============================  Daftar Pengumuman  =============================")
        print(df.to_markdown(index=False, tablefmt="heavy_grid"))
        
def cek_input_string(input_value):

    if not input_value.strip():
        return False
    try:
        float(input_value)
        return False
    except ValueError:
        return True

def add_announcement(file_name):
    initialize_csv(file_name)
    
    judul = input(Fore.YELLOW + "Masukkan judul pengumuman: ").strip()
    if not cek_input_string(judul):
        print(Fore.RED + "Inputan Harus Sesuai! (Judul harus berupa teks non-kosong)")
        return

    isi = input(Fore.YELLOW + "Masukkan isi pengumuman: ").strip()
    if not cek_input_string(isi):
        print(Fore.RED + "Inputan Harus Sesuai! (Isi harus berupa teks non-kosong)")
        return

    tanggal = input(Fore.YELLOW + "Masukkan tanggal pengumuman: ").strip()
    if not cek_input_string(tanggal):
        print(Fore.RED + "Inputan Harus Sesuai! (Tanggal harus berupa teks non-kosong)")
        return
    
    df = pd.read_csv(file_name)
    new_id = len(df) + 1
    df = pd.concat([df, pd.DataFrame({"ID": [new_id], "Judul": [judul], "Isi": [isi], "Tanggal": [tanggal]})])
    df.to_csv(file_name, index=False)
    clear_terminal()
    loading_masuk()
    clear_terminal()
    print(Fore.GREEN + "Pengumuman berhasil ditambahkan.")

def edit_announcement(file_name):
    initialize_csv(file_name)
    display_announcements(file_name)
    id_to_edit = input(Fore.YELLOW + "Masukkan ID pengumuman yang ingin diubah: ")
    df = pd.read_csv(file_name)
    if id_to_edit in df["ID"].astype(str).values:
        index = df[df["ID"] == int(id_to_edit)].index[0]
        try:
            judul = str(input(Fore.YELLOW + f"Masukkan judul baru (sebelumnya: {df.at[index, 'Judul']}): ") or df.at[index, "Judul"])
            isi = str(input(Fore.YELLOW + f"Masukkan isi baru (sebelumnya: {df.at[index, 'Isi']}): ") or df.at[index, "Isi"])
        except ValueError:
            print("")
            print(Fore.RED + "Inputan Harus Sesuai!")
            return
        
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
                clear_terminal()
                loading_masuk()
                clear_terminal()
                add_announcement(LOMBA_FILE)
            elif choice == "2":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                add_announcement(LIBUR_FILE)
            elif choice == "3":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                display_announcements(LOMBA_FILE)
            elif choice == "4":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                display_announcements(LIBUR_FILE)
            elif choice == "5":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                edit_announcement(LOMBA_FILE)
            elif choice == "6":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                edit_announcement(LIBUR_FILE)
            elif choice == "7":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                delete_announcement(LOMBA_FILE)
            elif choice == "8":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                delete_announcement(LIBUR_FILE)
            elif choice == "9":
                clear_terminal()
                loading_masuk()
                clear_terminal()
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
                clear_terminal()
                loading_masuk()
                clear_terminal()
                display_announcements(LOMBA_FILE)
            elif choice == "2":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                display_announcements(LIBUR_FILE)
            elif choice == "3":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                break
            else:
                print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")
                
###  FITUR 2  ###

def admin_manage_kehadiran():
    KEHADIRAN_FILE = initialize_kehadiran()
    df = pd.read_csv(KEHADIRAN_FILE, dtype={"nim": str})

    while True:
        print(Fore.CYAN + "\n=== KELOLA DATA KEHADIRAN ===")
        nim = input(Fore.YELLOW + "Masukkan NIM Mahasiswa yang Dicari: ")
        mahasiswa_data = df[df["nim"] == nim]

        if not mahasiswa_data.empty:
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.CYAN + "\nData Kehadiran Mahasiswa:")
            print(mahasiswa_data.to_markdown(index=False, tablefmt="heavy_grid"))
            
            print(Fore.CYAN + "1. Edit Data Kehadiran")
            print(Fore.CYAN + "2. Kembali")
            choice = input(Fore.YELLOW + "Pilih opsi: ")

            if choice == "1":
                id_to_edit = input(Fore.YELLOW + "Masukkan ID data yang ingin diubah: ")
                if id_to_edit in df["ID"].astype(str).values:
                    index = df[df["ID"] == int(id_to_edit)].index[0]
                    new_status = input(Fore.YELLOW + f"Masukkan status baru (sebelumnya: {df.at[index, 'status']}): ") or df.at[index, "status"]
                    df.at[index, "status"] = new_status.capitalize()
                    df.to_csv(KEHADIRAN_FILE, index=False)
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
    KEHADIRAN_FILE = initialize_kehadiran()
    df = pd.read_csv(KEHADIRAN_FILE, dtype={"nim": str})

    jadwal_matkul = {
        "Pemrograman Dasar": ("08:00", "09:00"),
        "Matematika Diskrit": ("10:00", "11:00"),
        "Sistem Operasi": ("13:00", "14:00"),
        "Struktur Data": ("16:00", "17:00"),
        "Kecerdasan Buatan": ("20:00", "21:00"),
    }

    print(Fore.CYAN + "\n=========  JADWAL MATA KULIAH  =========")
    for matkul, (start, end) in jadwal_matkul.items():
        print(Fore.YELLOW + f"- {matkul}: {start} - {end}")
        print(Fore.CYAN + "=" * 40)

    print("")
    print(Fore.CYAN + "\n==============  ABSENSI  ===============")
    current_time = datetime.now().strftime("%H:%M")
    print(Fore.GREEN + f"Waktu Sekarang: {current_time}")
    print(Fore.CYAN + "=" * 40)

    for matkul, (start, end) in jadwal_matkul.items():
        if start <= current_time <= end:
            print("")
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
                df.to_csv(KEHADIRAN_FILE, index=False)
                print(Fore.GREEN + f"Anda berhasil absen untuk mata kuliah {matkul}.")
        elif current_time < start:
            print(Fore.CYAN + f"Waktu absensi untuk mata kuliah {matkul} belum dimulai.")
        elif current_time > end:
            print(Fore.RED + f"Waktu absensi untuk mata kuliah {matkul} telah berlalu.")

    print(Fore.CYAN + "=" * 40)
    print(Fore.CYAN + "\nAbsensi selesai.")
    print("")

def data_kehadiran(role):
    if role == "admin":
        admin_manage_kehadiran()
    elif role == "mahasiswa":
        mahasiswa_absensi(role)
        
###   FITUR 3  ###

def tambah_nilai():
    initialize_nilai_file()
    df = pd.read_csv(NILAI_FILE)

    
    try:
        nim = str(input(Fore.YELLOW + "Masukkan NIM: "))
        nama = str(input(Fore.YELLOW + "Masukkan Nama Mahasiswa: "))
        matkul = str(input(Fore.YELLOW + "Masukkan Mata Kuliah: "))
        tugas = float(input(Fore.YELLOW + "Masukkan Nilai Tugas: "))
        uts = float(input(Fore.YELLOW + "Masukkan Nilai UTS: "))
        uas = float(input(Fore.YELLOW + "Masukkan Nilai UAS: "))
        
    except ValueError:
        print("")
        print(Fore.RED + "Inputan Harus Sesuai!")
        return
    

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

    data_mahasiswa = df[df["NIM"].astype(str).str.strip() == nim]
    clear_terminal()
    loading_masuk()
    clear_terminal()
    print(Fore.CYAN + Style.BRIGHT + "================================================  DATA NILAI ANDA  ================================================")
    print(Fore.WHITE + data_mahasiswa.to_markdown(index=False))
    print("")
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
        print("")
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
        print("")
        print(Fore.GREEN + "Data nilai berhasil dihapus.")
    else:
        print(Fore.RED + "ID tidak ditemukan.")

def data_nilai(role
               ):
    if role == "admin":
        while True:
            print(Fore.CYAN + "\n========= MANAJEMEN DATA NILAI =========")
            print(Fore.CYAN +"1. Tambah Nilai Mahasiswa")
            print(Fore.CYAN +"2. Lihat Nilai Mahasiswa")
            print(Fore.CYAN +"3. Edit Nilai Mahasiswa")
            print(Fore.CYAN +"4. Hapus Nilai Mahasiswa")
            print(Fore.RED + "5. Kembali")
            print(Fore.CYAN + "=" * 40)
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
        clear_terminal()
        loading_masuk()
        clear_terminal()
        print(Fore.CYAN + "\n=== DATA NILAI MAHASISWA ===")
        lihat_nilai()

### FITUR 4 ###

def kelola_ukt_admin():
    initialize_ukt_file()
    df = pd.read_csv(UKT_FILE, dtype={"NIM": str})

    while True:
        print(Fore.CYAN + "\n=== KELOLA STATUS UKT ===")
        nim = input(Fore.YELLOW + "Masukkan NIM mahasiswa: ").strip()

        if not nim.isdigit():
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.RED + "NIM tidak valid. Harus berupa angka.")
            continue

        mahasiswa = df[df["NIM"] == nim]

        if mahasiswa.empty:
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.RED + "Data tidak ditemukan. Tambahkan data baru.")
            nama = input(Fore.YELLOW + "Masukkan nama mahasiswa: ").strip()
            nominal_ukt = float(input(Fore.YELLOW + "Masukkan nominal UKT: "))
            status_pembayaran = input(Fore.YELLOW + "Masukkan status pembayaran (Lunas/Belum Lunas): ").capitalize()

            new_data = pd.DataFrame({
                "NIM": [nim],
                "NAMA": [nama],
                "NOMINAL": [nominal_ukt],
                "STATUS": [status_pembayaran]
            })
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(UKT_FILE, index=False)
            print(Fore.GREEN + "Data berhasil ditambahkan.")
        else:
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.CYAN + "\n========================  Data Mahasiswa  =======================")
            print("")
            print(mahasiswa.to_markdown(index=False, floatfmt=".0f", tablefmt="heavy_grid"))

            print(Fore.CYAN + "=" * 65)
            print(Fore.YELLOW + "1. Ubah Nominal UKT")
            print(Fore.YELLOW + "2. Ubah Status Pembayaran")
            print(Fore.YELLOW + "3. Cari Mahasiswa Lain")
            print(Fore.RED + "4. Kembali ke Menu Utama")
            print(Fore.CYAN + "=" * 65)
            pilihan = input(Fore.YELLOW + "Pilih opsi: ").strip()

            if pilihan == "1":
                try:
                    nominal_ukt = float(input(Fore.YELLOW + "Masukkan nominal UKT baru: "))
                    
                except ValueError:
                    print("")
                    print(Fore.RED + "Inputan Harus Berupa Angka!")
                    return
                
                df.loc[df["NIM"] == nim, "NOMINAL"] = nominal_ukt
                df.to_csv(UKT_FILE, index=False)
                print(Fore.GREEN + "Nominal UKT berhasil diubah.")
            elif pilihan == "2":
                status_pembayaran = str(input(Fore.YELLOW + "Masukkan status pembayaran baru (Lunas/Belum Lunas): ").capitalize())
                
                if not status_pembayaran == "Lunas" and "Belum Lunas":
                    print(Fore.RED + "Inputan Harus Sesuai!")
                    print("")
                    return
                
                df.loc[df["NIM"] == nim, "STATUS"] = status_pembayaran
                df.to_csv(UKT_FILE, index=False)
                print(Fore.GREEN + "Status pembayaran berhasil diubah.")
            elif pilihan == "3":
                continue
            elif pilihan == "4":
                break
            else:
                print(Fore.RED + "Pilihan tidak valid.")

def lihat_ukt_mahasiswa():
    initialize_ukt_file()
    df = pd.read_csv(UKT_FILE)
    nim = input(Fore.YELLOW + "Masukkan NIM Anda: ").strip()
    mahasiswa_ukt = df[df["NIM"].astype(str).str.strip() == nim]
    clear_terminal()
    loading_masuk()
    clear_terminal()
    print(Fore.CYAN + "\nData UKT Anda:")
    print(Fore.WHITE + mahasiswa_ukt.to_markdown(index=False, floatfmt=".0f", tablefmt="heavy_grid"))
    
    if mahasiswa_ukt.empty:
        clear_terminal()
        loading_masuk()
        clear_terminal()
        print(Fore.RED + "Data UKT tidak ditemukan.")

def pembayaran_ukt(role, nim):
    if role == "admin":
        kelola_ukt_admin()
    elif role == "mahasiswa":
        lihat_ukt_mahasiswa()
        
###  FITUR 5  ###

def admin_manage_ukm():
    initialize_ukm_file()
    while True:
        print(Fore.CYAN + "\n============== KELOLA DATA UKM ===============")
        print(Fore.CYAN + "1. Lihat Data UKM")
        print(Fore.CYAN + "2. Tambah Data UKM")
        print(Fore.CYAN + "3. Edit Status Perekrutan dan Informasi Lanjut")
        print(Fore.RED + "4. Kembali ke Menu Utama")
        print(Fore.CYAN + "=" * 46)
        choice = input(Fore.YELLOW + "Pilih opsi: ").strip()

        df = pd.read_csv(UKM_FILE)

        if choice == "1":
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.CYAN + "\nData UKM:")
            if df.empty:
                clear_terminal()
                loading_masuk()
                clear_terminal()
                print(Fore.RED + "Belum ada data UKM.")
            else:
                print(df.to_markdown(index=False, tablefmt="heavy_grid"))
        elif choice == "2":
            try:
                nama_ukm = str(input(Fore.YELLOW + "Masukkan nama UKM: ").strip())
                status = str(input(Fore.YELLOW + "Masukkan status perekrutan (Open Recruitment/Closed Recruitment): ").strip())
                info_lanjut = str(input(Fore.YELLOW + "Masukkan informasi lanjut (jika ada): ").strip())
            except ValueError:
                print(Fore.RED + "Inputan Harus Berupa Kalimat!")

            new_data = pd.DataFrame({
                "Nama UKM": [nama_ukm],
                "Status Perekrutan": [status],
                "Informasi Lanjut": [info_lanjut]
            })

            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(UKM_FILE, index=False)
            print(Fore.GREEN + "Data UKM berhasil ditambahkan.")
        elif choice == "3":
            print(Fore.CYAN + "\nData UKM:")
            print(df.to_markdown(index=False, tablefmt="heavy_grid"))
            nama_ukm = input(Fore.YELLOW + "Masukkan nama UKM yang ingin diedit: ").strip()

            if nama_ukm in df["Nama UKM"].values:
                index = df[df["Nama UKM"] == nama_ukm].index[0]

                new_status = input(Fore.YELLOW + f"Masukkan status perekrutan baru (sebelumnya: {df.at[index, 'Status Perekrutan']}): ") or df.at[index, "Status Perekrutan"]
                df.at[index, "Status Perekrutan"] = new_status

                if new_status.lower() == "open recruitment":
                    new_info = input(Fore.YELLOW + f"Masukkan informasi lanjut baru (sebelumnya: {df.at[index, 'Informasi Lanjut']}): ") or df.at[index, "Informasi Lanjut"]
                    df.at[index, "Informasi Lanjut"] = new_info

                df.to_csv(UKM_FILE, index=False)
                print(Fore.GREEN + "Data UKM berhasil diperbarui.")
            else:
                print(Fore.RED + "UKM tidak ditemukan.")
        elif choice == "4":
            break
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")

def mahasiswa_view_ukm():
    df = pd.read_csv(UKM_FILE)
    clear_terminal()
    loading_masuk()
    clear_terminal()
    print(Fore.CYAN + "\nData UKM:")
    print(df[['Nama UKM', 'Status Perekrutan']].to_markdown(index=False, tablefmt="heavy_grid"))

    nama_ukm = input(Fore.YELLOW + "Apakah Anda ingin mengetahui informasi lanjut tentang UKM tertentu? Masukkan nama UKM (atau tekan Enter untuk kembali): ").strip()

    if nama_ukm == "":
        clear_terminal()
        loading_masuk()
        clear_terminal()
        return
    
    elif nama_ukm in df["Nama UKM"].values:
        index = df[df["Nama UKM"] == nama_ukm].index[0]
        status = df.at[index, "Status Perekrutan"]

        if status.lower() == "open recruitment":
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.GREEN + f"\nUntuk mengikuti UKM {nama_ukm}, silahkan hubungi: {df.at[index, 'Informasi Lanjut']}.")
            print("")
        else:
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.RED + f"Maaf, UKM {nama_ukm} sedang tidak menerima perekrutan.")
            print("")
    else:
        clear_terminal()
        loading_masuk()
        clear_terminal()
        print(Fore.RED + "UKM tidak ditemukan.")
        print("")

def keorganisasian(role):
    if role == "admin":
        admin_manage_ukm()
    elif role == "mahasiswa":
        mahasiswa_view_ukm()

###  FITUR 6  ###

def tambah_dospem():
    initialize_dospem_file()
    df = pd.read_csv(DOSPEM_FILE, dtype={"NIM": str})

    try:
        nim = float(input(Fore.YELLOW + "Masukkan NIM Mahasiswa: "))
        nama = str(input(Fore.YELLOW + "Masukkan Nama Mahasiswa: "))
        dospem = str(input(Fore.YELLOW + "Masukkan Nama Dosen Pembimbing: "))
        penelitian = str(input(Fore.YELLOW + "Masukkan Penelitian (Optional): "))
    except ValueError:
        print(Fore.RED + "Inputan Harus Sesuai!")
        print("")
        return

    new_id = len(df) + 1 if not df.empty else 1

    new_data = pd.DataFrame({
        "ID": [new_id],
        "NIM": [nim],
        "Nama": [nama],
        "Dospem": [dospem],
        "Penelitian": [penelitian]
    })

    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DOSPEM_FILE, index=False)
    print(Fore.GREEN + "Data Dosen Pembimbing berhasil ditambahkan.")

def lihat_dospem(role,nim):
    initialize_dospem_file()
    df = pd.read_csv(DOSPEM_FILE, dtype={"NIM": str})

    if role == "admin":
        clear_terminal()
        loading_masuk()
        clear_terminal()
        print(Fore.CYAN + "\n=== SELURUH DATA DOSEN PEMBIMBING ===")
        if df.empty:
            print(Fore.RED + "Tidak ada data Dosen Pembimbing.")
        else:
            print(df.to_markdown(index=False, tablefmt="heavy_grid"))
    elif role == "mahasiswa":
        initialize_dospem_file()
        df = pd.read_csv(DOSPEM_FILE)
        nim = input(Fore.YELLOW + "Masukkan NIM Anda : ").strip()
        mahasiswa_dospem = df[df["NIM"].astype(str).str.strip() == nim]
        clear_terminal()
        loading_masuk()
        clear_terminal()
        print(Fore.CYAN + "\n=== DATA DOSEN PEMBIMBING ANDA ===")
        print(mahasiswa_dospem.to_markdown(index=False, tablefmt="heavy_grid"))
        print("")
        
        if mahasiswa_dospem.empty:
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.RED + "Anda belum memiliki data Dosen Pembimbing.")

def edit_dospem():
    initialize_dospem_file()
    df = pd.read_csv(DOSPEM_FILE, dtype={"NIM": str})

    clear_terminal()
    loading_masuk()
    clear_terminal()
    print(Fore.CYAN + "\n=== DATA DOSEN PEMBIMBING ===")
    print(df.to_markdown(index=False, tablefmt="heavy_grid"))
    
    id_to_edit = input(Fore.YELLOW + "Masukkan ID yang ingin diubah: ")

    if id_to_edit in df["ID"].astype(str).values:
        index = df[df["ID"] == int(id_to_edit)].index[0]

        dospem = input(Fore.YELLOW + f"Masukkan Nama Dosen Pembimbing baru (sebelumnya: {df.at[index, 'Dospem']}): ") or df.at[index, "Dospem"]
        penelitian = input(Fore.YELLOW + f"Masukkan Penelitian baru (sebelumnya: {df.at[index, 'Penelitian']}): ") or df.at[index, "Penelitian"]
        
        df.at[index, "Dospem"] = dospem
        df.at[index, "Penelitian"] = penelitian

        df.to_csv(DOSPEM_FILE, index=False)
        print(Fore.GREEN + "Data Dosen Pembimbing berhasil diperbarui.")
    else:
        print("")
        print(Fore.RED + "ID tidak ditemukan.")

def dosen_pembimbing(role, nim):
    if role == "admin":
        while True:
            print(Fore.CYAN + "\n=== MANAJEMEN DOSEN PEMBIMBING ===")
            print(Fore.CYAN + "1. Edit Data Dosen Pembimbing")
            print(Fore.CYAN + "2. Tambah Data Dosen Pembimbing")
            print(Fore.CYAN + "3. Lihat Semua Data")
            print(Fore.RED + "4. Keluar")
            print(Fore.CYAN + "=" * 34)
            
            pilihan = input(Fore.YELLOW + "Pilih opsi: ")
            
            if pilihan == "1":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                edit_dospem()
            elif pilihan == "2":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                tambah_dospem()
            elif pilihan == "3":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                lihat_dospem(role,nim)
            elif pilihan == "4":
                break
            else:
                print(Fore.RED + "Pilihan tidak valid.")
    elif role == "mahasiswa":
        lihat_dospem(role, nim)

###  FITUR 7  ###

def tambah_status():
    initialize_status_file()

    df = pd.read_csv(STATUS_FILE, dtype={"NIM": str})

    try:
        nim = float(input(Fore.YELLOW + "Masukkan NIM Mahasiswa: "))
        nama = str(input(Fore.YELLOW + "Masukkan Nama Mahasiswa: "))
        angkatan = float(input(Fore.YELLOW + "Masukkan Angkatan Mahasiswa: "))
        status = str(input(Fore.YELLOW + "Masukkan Status Kelulusan (Lulus/Belum Lulus): "))
        prestasi = str(input(Fore.YELLOW + "Masukkan Prestasi Mahasiswa : "))
    except ValueError:
        print("")
        print(Fore.RED + "Inputan Harus Sesuai!")
        return

    new_data = pd.DataFrame({
        "NIM": [nim],
        "Nama": [nama],
        "Angkatan": [angkatan],
        "Status Kelulusan": [status],
        "Prestasi": [prestasi]
    })

    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(STATUS_FILE, index=False)
    clear_terminal()
    loading_masuk()
    clear_terminal()
    print(Fore.GREEN + "Data Status Mahasiswa berhasil ditambahkan.")

def lihat_status(role,nim):
    initialize_status_file()
    df = pd.read_csv(STATUS_FILE, dtype={"NIM": str})

    if role == "admin":
        clear_terminal()
        loading_masuk()
        clear_terminal()
        print(Fore.CYAN + "\n=== SELURUH DATA STATUS MAHASISWA ===")
        if df.empty:
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.RED + "Tidak ada data Status Mahasiswa.")
        else:
            print(df.to_markdown(index=False, tablefmt="heavy_grid"))
    elif role == "mahasiswa":
        initialize_status_file()
        df = pd.read_csv(STATUS_FILE)
        
        try:
            nim = float(input(Fore.YELLOW + "Masukkan NIM Anda : ").strip())
        except ValueError:
            print("")
            print(Fore.RED + "NIM Harus Berupa Angka!")
            return
        
        mahasiswa_status = df[df["NIM"].astype(str).str.strip() == nim]
        clear_terminal()
        loading_masuk()
        clear_terminal()
        print(Fore.CYAN + "\n=== DATA STATUS MAHASISWA ANDA ===")
        print(mahasiswa_status.to_markdown(index=False, tablefmt="heavy_grid"))
        print("")
        
        if mahasiswa_status.empty:
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.RED + "Anda belum memiliki data Dosen Pembimbing.")

def edit_status():
    initialize_status_file()
    df = pd.read_csv(STATUS_FILE, dtype={"NIM": str})

    clear_terminal()
    loading_masuk()
    clear_terminal()
    print(Fore.CYAN + "\n=== DATA STATUS MAHASISWA ===")
    print(df.to_markdown(index=False, tablefmt="heavy_grid"))
    
    nim_to_edit = input(Fore.YELLOW + "Masukkan NIM yang ingin diubah: ")

    if nim_to_edit in df["NIM"].astype(str).values:
        index = df[df["NIM"] == int(nim_to_edit)].index[0]

        angkatan = input(Fore.YELLOW + f"Masukkan Angkatan baru (sebelumnya: {df.at[index, 'Angkatan']}): ") or df.at[index, "Angkatan"]
        status = input(Fore.YELLOW + f"Masukkan Status baru (sebelumnya: {df.at[index, 'Status Kelulusan']}): ") or df.at[index, "Status kelulusan"]
        prestasi = input(Fore.YELLOW + f"Masukkan Prestasi baru (sebelumnya: {df.at[index, 'Prestasi']}): ") or df.at[index, "Prestasi"]

        df.at[index, "Angkatan"] = angkatan
        df.at[index, "Status Kelulusan"] = status
        df.at[index, "Prestasi"] = prestasi

        df.to_csv(STATUS_FILE, index=False)
        print(Fore.GREEN + "Data Status Mahasiswa berhasil diperbarui.")
    else:
        print(Fore.RED + "NIM tidak ditemukan.")

def status_mahasiswa(role, nim):
    if role == "admin":
        while True:
            print(Fore.CYAN + "\n=== PENGATURAN STATUS MAHASISWA ===")
            print(Fore.CYAN + "1. Edit Data Status Mahasiswa")
            print(Fore.CYAN + "2. Tambah Data Status Mahasiswa")
            print(Fore.CYAN + "3. Lihat Semua Data")
            print(Fore.RED + "4. Keluar")
            
            pilihan = input(Fore.YELLOW + "Pilih opsi: ")
            
            if pilihan == "1":
                edit_status()
            elif pilihan == "2":
                tambah_status()
            elif pilihan == "3":
                lihat_status(role,nim)
            elif pilihan == "4":
                break
            else:
                print(Fore.RED + "Pilihan tidak valid.")
    elif role == "mahasiswa":
        lihat_status(role, nim)
        
###  BATAS CODE FITUR  ###    

def menu(role, nim):
    clear_terminal()
    loading_masuk()
    clear_terminal()
    print(Fore.BLUE + text2art("MAHALINK", font="block"))
    print(Fore.GREEN + f"                                                       Anda Telah Berhasil Login Sebagai {role.capitalize()}!")
    print(Fore.CYAN + "=" * 40)
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
                clear_terminal()
                loading_masuk()
                clear_terminal()
                pengumuman_akademik(role)
            elif choice == "2":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                data_kehadiran(role)
            elif choice == "3":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                data_nilai(role,nim)
            elif choice == "4":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                pembayaran_ukt(role,nim)
            elif choice == "5":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                keorganisasian(role)
            elif choice == "6":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                dosen_pembimbing(role,nim)
            elif choice == "7":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                status_mahasiswa(role,nim)
            elif choice == "8":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                print(Fore.GREEN + "Anda telah keluar dari menu.")
                break
            else:
                print(Fore.CYAN + f"Anda memilih opsi {choice}. (Fitur ini belum tersedia)")
        elif role == "mahasiswa":
            if choice == "1":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                pengumuman_akademik(role)
            elif choice == "2":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                mahasiswa_absensi(nim)
            elif choice == "3":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                data_nilai(role,nim)
            elif choice == "4":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                pembayaran_ukt(role,nim)
            elif choice == "5":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                keorganisasian(role)
            elif choice == "6":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                dosen_pembimbing(role,nim)
            elif choice =="7":
                clear_terminal()
                loading_masuk()
                clear_terminal()
                status_mahasiswa(role,nim)
            elif choice == "8":
                clear_terminal()
                loading_masuk()
                clear_terminal()
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
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.RED + "NIM sudah terdaftar! Silakan gunakan NIM lain.")
        else:
            role = "admin" if nim == "4646" else "mahasiswa"
            new_data = pd.DataFrame({"nim": [nim], "password": [password], "role": [role]})
            new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.GREEN + f"Anda Sudah Berhasil Mendaftar Sebagai {role.capitalize()}, Silakan Login.")
    else:
        clear_terminal()
        loading_masuk()
        clear_terminal()
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
            clear_terminal()
            loading_masuk()
            clear_terminal()
            print(Fore.RED + "Password salah!")
            print(Fore.CYAN + "=" * 40)
    else:
        clear_terminal()
        loading_masuk()
        clear_terminal()
        print(Fore.RED + "NIM tidak ditemukan!")
        print(Fore.CYAN + "=" * 40)
    return None, None

def main():
    print(Fore.CYAN + "=" * 40)
    print(Fore.BLUE + Style.BRIGHT + "~~~ SELAMAT DATANG ~~~")
    print(Fore.CYAN + "=" * 40)
    while True:
        print(Fore.CYAN + "1. Registrasi")
        print(Fore.CYAN + "2. Login")
        print(Fore.RED + "3. Keluar")
        print(Fore.CYAN + "=" * 40)
        choice = input(Fore.YELLOW + "Pilihlah opsi (1/2/3): ")
        
        if choice == '1':
            clear_terminal()
            loading_masuk()
            clear_terminal()
            register_as_mahasiswa()
        elif choice == '2':
            clear_terminal()
            loading_masuk()
            clear_terminal()
            user_role, user_nim = login()
            if user_role:
                menu(user_role, user_nim)
        elif choice == '3':
            clear_terminal()
            loading_dots()
            clear_terminal()
            print(Fore.BLUE + text2art("Terimah Kasih!", font="small"))
            print(Fore.GREEN + Style.BRIGHT + ("                Telah Menggunakan Aplikasi MahaLink :D"))
            print("")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
