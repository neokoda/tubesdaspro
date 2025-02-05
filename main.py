import os, sys, math, time, argparse, datetime
import typing
from utils import *
from models import *

# F01 - Login
# Input: current user logged in, matriks user 
def login(users: Array) -> None:
    global LOGGED_IN, ALLOWED_COMMANDS
    if LOGGED_IN.nama == None:
        username = input("Username: ")
        password = input("Password: ")
        
        found_index = search_nama(users, username)
        if found_index != -1:
            if users.arr[found_index].pwd == password:
                print()
                print(f"Selamat datang, {username}!")
                print('Masukkan command "help" untuk daftar command yang dapat kamu panggil.')
                LOGGED_IN = users.arr[found_index]
                if LOGGED_IN.role == "bandung_bondowoso":
                    ALLOWED_COMMANDS = BANDUNG_COMMANDS
                elif LOGGED_IN.role == "roro_jonggrang":
                    ALLOWED_COMMANDS = RORO_COMMANDS
                elif LOGGED_IN.role == "jin_pembangun":
                    ALLOWED_COMMANDS = PEMBANGUN_COMMANDS
                else:
                    ALLOWED_COMMANDS = PENGUMPUL_COMMANDS
            else:
                print("Password salah!")
        else:
            print("Username tidak terdaftar!")
    else:
        print("Login gagal!")
        print(f'Anda telah login dengan username {LOGGED_IN.nama}, silakan lakukan "logout" sebelum melakukan login kembali.')

# F02 - Logout
# Input: current user logged in
def logout() -> None:
    global LOGGED_IN
    if LOGGED_IN.nama != None:
        LOGGED_IN = User([None for i in range(3)])
    else:
        print("Logout gagal!")
        print("Anda belum login, silakan login terlebih dahulu sebelum melakukan logout")
        
# F03 - Summon Jin
# Input: matriks user
def summonjin() -> None:
    global users
    if users.neff < 102:
        print("""Jenis jin yang dapat dipanggil:
            (1) Pengumpul - Bertugas mengumpulkan bahan bangunan
            (2) Pembangun - Bertugas membangun candi
        """)
        jenis_jin = ""
        while jenis_jin != "1" and jenis_jin != "2":
            print()
            jenis_jin = input("Masukkan nomor jenis jin ingin dipanggil: ")
            if jenis_jin != "1" and jenis_jin != "2":
                print()
                print(f'Tidak ada jenis jin bernomor "{jenis_jin}"!')
        if jenis_jin == "1":
            print()
            print('Memilih jin "Pengumpul"')
            jenis_jin = "jin_pengumpul"
        else:
            print()
            print('Memilih jin "Pembangun"')
            jenis_jin = "jin_pembangun"
        print()
        username = input("Masukkan username jin: ")
        while search_nama(users, username) != -1:
            print(f'\nUsername "{username}" sudah diambil!\n')
            username = input("Masukkan username jin: ")
                
        valid = False
        while not valid:
            password = input("Masukkan password jin: ")
            if len(password) < 5 or len(password) > 25:
                print("\nPassword panjangnya harus 5-25 karakter!\n")
            else:
                valid = True
        
        print("\nMengumpulkan sesajen...")
        print("Menyerahkan sesajen...")
        print("Membacakan mantra...")
        
        jin_baru = User([username, password, jenis_jin])
        insert_empty(users, jin_baru)
        
        print()
        print(f"Jin {username} berhasil dipanggil!")
    else:
        print("Jumlah Jin telah maksimal! (100 jin). Bandung tidak dapat men-summon lebih dari itu")

# F04 - Hilangkan Jin
# Input: matriks user
def hapusjin() -> None:
    global users
    username = input("Masukkan username jin: ")
    found_index = search_nama(users, username)
    
    if found_index != -1:
        choice = binary_question(f"Apakah anda yakin ingin menghapus jin dengan username {username} (Y/N)? ")
        if choice == "Y":
            print("\nJin telah berhasil dihapus dari alam gaib.")
            # TODO add removing mechanism, remember to remove candi made by said jin (to implement undo, save jin+candi to an array, make a model for it?)
    else:
        print("\nTidak ada jin dengan username tersebut.")
            
# F05 - Ubah Tipe Jin
# Input: users
def ubahjin() -> None:
    global users
    username = input("Masukkan username jin: ")
    found_index = search_nama(users, username)
    
    if found_index != -1 and users.arr[found_index].role != "bandung_bondowoso" and users.arr[found_index].role != "roro_jonggrang":
        if users.arr[found_index].role == "jin_pembangun":
            choice = binary_question('Jin ini bertipe "Pembangun". Yakin ingin mengubah ke tipe "Pengumpul" (Y/N)? ')
            if choice == "Y":
                users.arr[found_index].role = "jin_pengumpul"
                print("\nJin telah berhasil diubah.")
        else:
            choice = binary_question('Jin ini bertipe "Pengumpul". Yakin ingin mengubah ke tipe "Pembangun" (Y/N)? ')
            if choice == "Y":
                users.arr[found_index].role = "jin_pembangun"
                print("\nJin telah berhasil diubah.")
    else:
        print("\nTidak ada jin dengan username tersebut.")
        
# F06 - Jin Pembangun
# Input: logged in user, 
def bangun() -> None:
    global LOGGED_IN, bahan_bangunan
    pass

# F07 - Jin Pengumpul
# Input: logged in user
def bangun() -> None:
    pass

# F08 - Batch Bangun/Kumpul
# Input: logged in user
def batchbangun() -> None:
    pass

def batchkumpul() -> None:
    pass

# F09 - Laporan Jin
# Input: matriks jin, matriks candi, matriks bahan bangunan
def laporanjin() -> None:
    pass

# F10 - Laporan Candi
# Input: matriks candi
def laporancandi() -> None:
    pass

# F11 - Hancurkan Candi
# Input: matriks candi
def hancurkancandi() -> None:
    global candi
    id_candi = int(input("Masukkan ID candi: "))
    found_index = search_id(candi, id_candi)
    
    if found_index != -1:
        choice = binary_question(f"Apakah Anda yakin ingin menghancurkan candi ID: {id_candi} (Y/N)? ")
        if choice == "Y":
            candi = rmv(candi, found_index)
            print("\nCandi telah berhasil dihancurkan.")
    else:
        print("\nTidak ada candi dengan ID tersebut.")

# F12 - Ayam Berkokok
# Input: matriks candi
def ayamberkokok() -> None:
    global candi
    print("Kukuruyuk.. Kukuruyuk..")
    print(f"\nJumlah Candi: {candi.neff}\n")
    if candi.neff < 100:
        print("Selamat, Roro Jonggrang memenangkan permainan!\n")
        print("*Bandung Bondowoso angry noise*")
        print("Roro Jonggrang dikutuk menjadi candi.")
        sys.exit()
    else:
        print("Yah, Bandung Bondowoso memenangkan permainan!")
        sys.exit()
    

# F13 - Load
# Input: nama folder, 
def load(path : str) -> None:
    global users, candi, bahan_bangunan
    folder_path = os.path.join(os.path.dirname(__file__), "save", path)
    if os.path.isdir(folder_path):
        print("Loading...")
        users = csv_parser(folder_path, "user.csv", users)
        candi = csv_parser(folder_path, "candi.csv", candi)
        bahan_bangunan = csv_parser(folder_path, "bahan_bangunan.csv", bahan_bangunan)
        print('Selamat datang di program "Manajerial Candi"')
        
    else:
        print(f'Folder "{path}" tidak ditemukan.')
        sys.exit()

# F14 - Save
# Input: logged in user
def save() -> None:
    global users, candi, bahan_bangunan
    print()
    folder = input("Masukkan nama folder: ")
    folder_path = os.path.join(os.path.dirname(__file__), "save", folder)
    print("\nSaving...")
    if not os.path.isdir(folder_path):
        print(f"\nMembuat folder save/{folder}")
        os.mkdir(folder_path)
    csv_writer(folder_path, users, candi, bahan_bangunan)
    print(f"\nBerhasil menyimpan data di folder save/{folder}!")

# F15 - Help
# Input: logged in user
def help(commands : Array) -> None:
    print("=========== HELP ===========")
    for i in range(commands.neff):
        print(f"{i+1}. {commands.arr[i].nama}")
        print(f"   {commands.arr[i].deskripsi}")

# F16 - Exit
# Input: logged in user
def exit() -> None:
    choice = binary_question("Apakah Anda mau melakukan penyimpanan file yang sudah diubah (Y/N)? ")
    if choice == "Y":
        save()
    sys.exit()
    
# B04 - Undo
# Input: jin purg, candi purg
def undo() -> None:
    global jin_purgatory, candi_purgatory
    pass
# -----------------------=====================================----------------------------------

# Variabel berisi akun yang sedang login dan commandsnya
LOGGED_IN = User([None for i in range(3)]) # Simpan user yang login
ALLOWED_COMMANDS = DEFAULT_COMMANDS

# Parser untuk input nama folder
parser = argparse.ArgumentParser()
parser.add_argument("nama_folder", help="Folder berisi data csv", nargs='?', default=None)
args = parser.parse_args()

# Array data user, candi, dan bahan bangunan
users = Array([[None for i in range(NMAX)], 0])
candi = Array([[None for i in range(NMAX)], 0])
bahan_bangunan = Array([[None for i in range(NMAX)], 0])

# Array jin dan candi yang telah dihapus
jin_purgatory = Array([[None for i in range(NMAX)], 0])
candi_purgatory = Array([[None for i in range(NMAX)], 0])

# Run ketika file di call
if __name__ == "__main__":
    if args.nama_folder:
        # Load file csv
        load(args.nama_folder)
        # Main loop command
        while True:
            cmd = input(">>> ")
            if cmd == "login":
                login(users)
            elif cmd == "help":
                help(ALLOWED_COMMANDS)
            elif cmd == "logout":
                logout()
            elif cmd == "debug":
                print_user(users)
    else:
        print("Tidak ada nama folder yang diberikan!")
        print()
        print("Usage: python main.py <nama_folder>")
        sys.exit()
        
