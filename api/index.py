from http.server import BaseHTTPRequestHandler
import cloudscraper
import base64
import re
from Crypto.Cipher import AES
import json

def decrypt_payload(ciphertext, key_hex, iv_hex):
    try:
        key = bytes.fromhex(key_hex)
        iv = bytes.fromhex(iv_hex)
        cipher = AES.new(key, 2, iv)
        decrypted_raw = cipher.decrypt(base64.b64decode(ciphertext))
        decrypted_text = decrypted_raw.decode('utf-8', errors='ignore')
        found = re.findall(r'https?://[^\s<>"]+', decrypted_text)
        if found:
            link = found[0].replace('\\', '')
            return "".join(char for char in link if 31 < ord(char) < 127)
    except:
        return None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        api_url = "https://www.elahmad.org/tv/live/shahid_shaka.php"
        payload = {"id": "dubaione"}
        
        # إضافة Headers مطابقة تماماً للمتصفح
        headers = {
            "Origin": "https://www.elahmad.org",
            "Referer": "https://www.elahmad.org/",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        
        try:
            resp = scraper.post(api_url, data=payload, headers=headers, timeout=10)
            data = resp.json()
            link = decrypt_payload(data.get('link_4'), data.get('key'), data.get('iv'))
            
            if link:
                # توجيه مباشر للبث
                self.send_response(302)
                self.send_header('Location', link)
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.end_headers()
            else:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Error: Could not extract link. Data received but decryption failed.")
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())
