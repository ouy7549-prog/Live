from flask import Flask, redirect, Response
import cloudscraper
import base64
import re
from Crypto.Cipher import AES

app = Flask(__name__)

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

@app.route('/')
@app.route('/api')
def get_stream():
    scraper = cloudscraper.create_scraper()
    api_url = "https://www.elahmad.org/tv/live/shahid_shaka.php"
    payload = {"id": "dubaione"}
    headers = {"Referer": "https://www.elahmad.org/"}
    
    try:
        resp = scraper.post(api_url, data=payload, headers=headers)
        data = resp.json()
        link = decrypt_payload(data.get('link_4'), data.get('key'), data.get('iv'))
        
        if link:
            return redirect(link)
        return "Error: Link not found", 500
    except Exception as e:
        return f"Error: {str(e)}", 500

# مهم جداً لـ Vercel
app.debug = True
