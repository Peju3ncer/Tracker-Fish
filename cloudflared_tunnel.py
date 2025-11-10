import subprocess
import sys
import os
import re
import time

def check_cloudflared():
    """Memeriksa apakah cloudflared terinstall"""
    try:
        subprocess.run(['cloudflared', '--version'], capture_output=True)
        return True
    except FileNotFoundError:
        return False

def get_tunnel_url(process):
    """Mendapatkan URL tunnel dari output cloudflared"""
    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.decode('utf-8').strip()
        # Mencari URL tunnel dalam output
        if 'https://' in line and '.trycloudflare.com' in line:
            match = re.search(r'https://[^\s]+\.trycloudflare\.com', line)
            if match:
                return match.group(0)
        # Mencari pesan error umum
        elif 'error' in line.lower():
            raise Exception(f"Cloudflared error: {line}")
    return None

def start_cloudflared_tunnel(port):
    """Memulai Cloudflared tunnel"""
    if not check_cloudflared():
        print("\n[X] Cloudflared tidak ditemukan!")
        print("\nUntuk menginstall cloudflared:")
        print("1. Windows: Unduh dari https://github.com/cloudflare/cloudflared/releases")
        print("2. Linux: curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb")
        print("   Lalu: sudo dpkg -i cloudflared.deb")
        print("3. Mac: brew install cloudflared")
        sys.exit(1)

    try:
        process = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        print("\n[⌛] Memulai Cloudflared tunnel...")
        
        # Tunggu beberapa detik untuk memastikan tunnel dimulai
        time.sleep(3)
        
        tunnel_url = None
        for line in process.stdout:
            if 'https://' in line and '.trycloudflare.com' in line:
                match = re.search(r'https://[^\s]+\.trycloudflare\.com', line)
                if match:
                    tunnel_url = match.group(0)
                    break
            elif 'error' in line.lower():
                raise Exception(f"Cloudflared error: {line}")
            print(line.strip())  # Tampilkan output cloudflared

        if tunnel_url:
            print(f"\n[✓] Tunnel berhasil dibuat!")
            print(f"[🌐] URL Tunnel: {tunnel_url}")
            return process
        else:
            raise Exception("Tidak bisa mendapatkan URL tunnel")

    except Exception as e:
        print(f"\n[X] Error saat membuat tunnel: {str(e)}")
        print("\nSolusi yang mungkin:")
        print("1. Pastikan cloudflared sudah terinstall dengan benar")
        print("2. Cek koneksi internet Anda")
        print("3. Pastikan port tidak diblokir firewall")
        print("4. Coba jalankan 'cloudflared tunnel --url http://localhost:8080' secara manual")
        print("5. Periksa log cloudflared untuk detail error")
        sys.exit(1)

def stop_cloudflared_tunnel(process):
    """Menghentikan Cloudflared tunnel"""
    if process:
        process.terminate()
        try:
            process.wait(timeout=5)  # Tunggu proses selesai
        except subprocess.TimeoutExpired:
            process.kill()  # Force kill jika timeout
        print("\n[✓] Cloudflared tunnel dihentikan")