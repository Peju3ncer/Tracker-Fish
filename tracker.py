#!/usr/bin/env python3
# tracker.py - Localhost mode + logging
import http.server
import socketserver
import os
import time
import signal
import sys
import platform
from datetime import datetime
from urllib.parse import urlparse
from shutil import which
import logging
from logging.handlers import RotatingFileHandler
import threading

# =========================
# KONFIGURASI
# =========================
PORT = 8080
FOLDER_NAME = "server"
CLEAR_COMMAND = "clear" if os.name == "posix" else "cls"
LOG_FILENAME = "tracker.log"
MAX_LOG_BYTES = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3

# Global server handle supaya bisa shutdown dari signal handler
httpd = None

# =========================
# UTILITAS TERMINAL & LOG
# =========================
def clear_screen():
    try:
        os.system(CLEAR_COMMAND)
    except Exception:
        pass

def print_banner():
    print("=" * 40)
    print("     TRACKER FISH                  ")
    print("  By: Peju 3ncer                   ")
    print("=" * 40)

def setup_logging(log_path):
    logger = logging.getLogger("tracker")
    logger.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(ch_formatter)

    # Rotating file handler
    fh = RotatingFileHandler(log_path, maxBytes=MAX_LOG_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(ch_formatter)

    # Avoid duplicate handlers on re-run
    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

# =========================
# CEK & MASUK KE FOLDER SERVER
# =========================
def cek_folder_server():
    try:
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FOLDER_NAME)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Folder '{FOLDER_NAME}' tidak ditemukan: {full_path}")
        os.chdir(full_path)
        return full_path
    except Exception as e:
        print(f"[X] Gagal mengakses folder server: {e}")
        sys.exit(1)

def tampilkan_info_sistem(logger):
    logger.info(f"Platform   : {platform.system()} {platform.machine()}")
    logger.info(f"Sekarang   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Direktori  : {os.getcwd()}")
    logger.info(f"Port       : {PORT}")

# =========================
# HANDLER KUSTOM UNTUK REQUESTS
# =========================
class LoggingHandler(http.server.SimpleHTTPRequestHandler):
    server_version = "TrackerFishHTTP/1.0"

    def _log_request_full(self, note=""):
        # Common details to log about a request
        client = f"{self.client_address[0]}:{self.client_address[1]}"
        method = self.command
        path = self.path
        parsed = urlparse(path)
        return f"{client} | {method} | {parsed.path} | query={parsed.query} {note}"

    def do_GET(self):
        logger = logging.getLogger("tracker")
        logger.info(self._log_request_full())
        # Serve files as usual from current directory
        try:
            super().do_GET()
        except Exception as e:
            logger.error(f"Error saat men-serv file: {e}")
            self.send_error(500, "Internal Server Error")

    def do_POST(self):
        logger = logging.getLogger("tracker")
        note = ""
        try:
            length = int(self.headers.get('Content-Length', 0))
            content_type = self.headers.get('Content-Type', '')
            data = self.rfile.read(length) if length > 0 else b""
            try:
                decoded = data.decode('utf-8', errors='replace')
            except Exception:
                decoded = repr(data)
            note = f"| content-type={content_type} | payload_len={len(data)}"
            logger.info(self._log_request_full(note))
            logger.info("---- BEGIN POST PAYLOAD ----")
            logger.info(decoded)
            logger.info("----  END POST PAYLOAD  ----")
            # respond OK
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            logger.error(f"[X] Gagal menangani POST: {e}")
            try:
                self.send_response(500)
                self.end_headers()
            except:
                pass

    def log_message(self, format, *args):
        # Matikan default stdout dari SimpleHTTPRequestHandler (kita handle sendiri)
        return

# =========================
# SERVER STARTER (Threaded)
# =========================
class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

def mulai_server(logger):
    global httpd
    try:
        with ThreadingHTTPServer(("127.0.0.1", PORT), LoggingHandler) as httpd_local:
            httpd = httpd_local
            addr = httpd.server_address
            logger.info(f"[√] Server aktif di: http://{addr[0]}:{addr[1]}")
            logger.info("[⌛] Menunggu koneksi... (akses hanya dari localhost)\n")
            try:
                httpd.serve_forever()
            except Exception as e:
                logger.error(f"[X] Error saat serve_forever: {e}")
    except OSError as e:
        logger.error(f"[X] Port {PORT} sedang digunakan atau akses ditolak: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"[X] Error saat menjalankan server: {e}")
        sys.exit(1)

# =========================
# EXIT HANDLER (Ctrl+C / SIGTERM)
# =========================
def handle_exit(sig, frame):
    logger = logging.getLogger("tracker")
    logger.info("\n[!] Dihentikan oleh user (signal received).")
    global httpd
    try:
        if httpd:
            logger.info("[⌛] Menghentikan server...")
            threading.Thread(target=httpd.shutdown).start()
            # beri waktu sebentar agar shutdown terjadi
            time.sleep(0.5)
    except Exception as e:
        logger.error(f"[X] Gagal shutdown server secara rapi: {e}")
    logger.info("[✓] Semua koneksi dihentikan. Keluar dengan aman.")
    sys.exit(0)

# =========================
# MAIN FUNCTION
# =========================
def main():
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    clear_screen()
    print_banner()

    # cek folder server & pindah
    full_path = cek_folder_server()

    # siapkan logging (file ada di folder server)
    log_path = os.path.join(full_path, LOG_FILENAME)
    logger = setup_logging(log_path)

    tampilkan_info_sistem(logger)

    try:
        user_input = input("\nMasukkan password untuk mulai: ").strip().lower()
        if user_input != "masuk":
            logger.info("[!] Tidak dikenali, akses ditolak. Program dibatalkan.")
            sys.exit(0)
    except KeyboardInterrupt:
        handle_exit(None, None)

    logger.info("[🔐] Mode: LOCALHOST (tidak membuat tunnel external)")
    logger.info(f"[📁] Log file: {log_path}")
    logger.info("[🔎] Memulai server dan logging aktivitas...")

    mulai_server(logger)

if __name__ == "__main__":
    main()
