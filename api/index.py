from http.server import BaseHTTPRequestHandler
import cloudscraper
import base64
import re
from Crypto.Cipher import AES

def decrypt_payload(ciphertext, key_hex, iv_hex):
    key = bytes.fromhex(key_hex)
    iv = bytes.fromhex(iv_hex)
    cipher = AES.new(key, 2, iv)
    decrypted_raw = cipher.decrypt(base64.b64decode(ciphertext))
    decrypted_text = decrypted_raw.decode('utf-8', errors='ignore')
    found = re.findall(r'https?://[^\s<>"]+', decrypted_text)
    if found:
        link = found[0].replace('\\', '')
        return "".join(char for char in link if 31 < ord(char) < 127)
    return None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        scraper = cloudscraper.create_scraper()
        api_url = "https://www.elahmad.org/tv/live/shahid_shaka.php"
        payload = {"id": "dubaione"}
        headers = {"Referer": "https://www.elahmad.org/"}
        
        try:
            resp = scraper.post(api_url, data=payload, headers=headers)
            data = resp.json()
            link = decrypt_payload(data['link_4'], data['key'], data['iv'])
            
            if link:
                # هذا هو الجزء السحري: توجيه المشغل للرابط فوراً
                self.send_response(302)
                self.send_header('Location', link)
                self.end_headers()
            else:
                self.send_response(500)
                self.end_headers()
        except:
            self.send_response(500)
            self.end_headers()
