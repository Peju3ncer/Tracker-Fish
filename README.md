# 🐟 Tracker-Fish

**Tracker-Fish** adalah proyek pelacakan perangkat berbasis umpan (honeypot phishing) yang digunakan untuk mendeteksi informasi dasar dari perangkat target melalui halaman umpan (bait page). Alat ini dibuat untuk keperluan edukasi keamanan siber dan simulasi penetration testing, **bukan untuk disalahgunakan**.

> ❗️**Peringatan:** Penggunaan proyek ini untuk tujuan jahat atau tanpa izin eksplisit dari pemilik perangkat merupakan pelanggaran hukum.

---

# 🧠 Cara Kerja

1. Server lokal dibuat menggunakan Python `http.server` dan ditampilkan ke publik menggunakan [Ngrok](https://ngrok.com/).
2. Target akan diarahkan ke halaman umpan (mirip tampilan transfer PayPal sukses).
3. Saat target membuka halaman, script akan:
   - Mengambil data **user agent**, **platform**, dan **bahasa**.
   - Mengambil **status baterai**.
   - Meminta akses **lokasi GPS** (jika diizinkan).
4. Data dikirim kembali ke server melalui request `POST`.

---

# 📁 Struktur Proyek
Tracker-Fish/
├── README.md
├── tracker.py
└── server/
    ├── index.html
    ├── style.css
    └── script.js
    ---

# ▶️ Cara Menjalankan

### 1. Pastikan Python & Ngrok sudah terinstal
- Install Python: [https://python.org](https://python.org)
- Install Ngrok: [https://ngrok.com](https://ngrok.com)

### 2. Install `pyngrok`
```bash
pip install pyngrok
```
### 3. Jalankan Server :
```bash
python tracker.py
```
## ATTENTION!!!
-
# ⚠️ Legal & Etika
---
##### Proyek ini hanya untuk:

• Simulasi keamanan
• Penelitian edukasi
• Demonstrasi keamanan perangkat

##### Dilarang menggunakan Tracker-Fish untuk:

• Memata-matai orang tanpa izin
• Menjebak pengguna secara ilegal
• Aktivitas kriminal lainnya


### Jika digunakan secara tidak sah, pencipta proyek tidak bertanggung jawab atas akibatnya.
```bash
---
👨‍💻 Dibuat oleh

🗥️ Peju 3ncer
Untuk edukasi dan pertahanan digital
---
