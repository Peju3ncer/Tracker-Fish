#!/usr/bin/env python3

# Daftar kode HTML yang tersedia
html_options = {
    1: """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Halaman Sederhana</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { color: blue; }
    </style>
</head>
<body>
    <h1>Selamat Datang di Halaman Sederhana</h1>
    <p>Ini adalah contoh halaman HTML dasar.</p>
</body>
</html>
""",
    2: """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form Kontak</title>
    <style>
        form { max-width: 400px; margin: auto; padding: 20px; border: 1px solid #ccc; }
        input, textarea { width: 100%; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>Form Kontak</h1>
    <form action="#" method="post">
        <label for="name">Nama:</label>
        <input type="text" id="name" name="name" required>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>
        <label for="message">Pesan:</label>
        <textarea id="message" name="message" rows="4" required></textarea>
        <button type="submit">Kirim</button>
    </form>
</body>
</html>
""",
    3: """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daftar Tugas</title>
    <style>
        ul { list-style-type: none; padding: 0; }
        li { padding: 10px; border-bottom: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>Daftar Tugas</h1>
    <ul>
        <li>Belajar Python</li>
        <li>Membuat proyek HTML</li>
        <li>Menguji aplikasi</li>
    </ul>
</body>
</html>
"""
}

def print_colored_ascii():
    ascii_art = """
░██████████                               ░██                                   ░██████████░██           ░██        
    ░██                                   ░██                                   ░██                      ░██        
    ░██    ░██░████  ░██████    ░███████  ░██    ░██ ░███████  ░██░████         ░██        ░██ ░███████  ░████████  
    ░██    ░███           ░██  ░██    ░██ ░██   ░██ ░██    ░██ ░███     ░██████ ░█████████ ░██░██        ░██    ░██ 
    ░██    ░██       ░███████  ░██        ░███████  ░█████████ ░██              ░██        ░██ ░███████  ░██    ░██ 
    ░██    ░██      ░██   ░██  ░██    ░██ ░██   ░██ ░██        ░██              ░██        ░██       ░██ ░██    ░██ 
    ░██    ░██       ░█████░██  ░███████  ░██    ░██ ░███████  ░██              ░██        ░██ ░███████  ░██    ░██ 

    𝕍𝕖𝕣𝕤𝕚𝕠𝕟: 𝕧𝟚.𝟘
    𝕄𝕒𝕕𝕖 𝔹𝕪: ℙ𝕖𝕛𝕦𝟛𝕟𝕔𝕖𝕣
"""
    colors = ['\033[31m', '\033[33m', '\033[32m', '\033[36m', '\033[34m', '\033[35m', '\033[37m']  # red, yellow, green, cyan, blue, magenta, white
    lines = ascii_art.strip().split('\n')
    for i, line in enumerate(lines):
        if i < 7:  # first 7 lines rainbow
            print(colors[i % len(colors)] + line + '\033[0m')
        else:
            print(line)  # version and made by in default color

def main():
    print_colored_ascii()
    print("Pilih kode HTML yang ingin di-generate:")
    print("Nomor | Nama Kode")
    print("------|----------")
    print("1     | Halaman Sederhana")
    print("2     | Form Kontak")
    print("3     | Daftar Tugas")
    print()
    
    try:
        choice = int(input("Masukkan nomor pilihan (1-3): "))
        if choice in html_options:
            print("\nKode HTML yang dipilih:\n")
            print(html_options[choice])
        else:
            print("Pilihan tidak valid.")
    except ValueError:
        print("Masukkan angka yang valid.")

if __name__ == "__main__":
    main()