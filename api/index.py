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

# ... نفس دوال التشفير السابقة ...

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        scraper = cloudscraper.create_scraper()
        api_url = "https://www.elahmad.org/tv/live/shahid_shaka.php"
        payload = {"id": "dubaione"}
        headers = {
            "Referer": "https://www.elahmad.org/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        
        try:
            resp = scraper.post(api_url, data=payload, headers=headers)
            data = resp.json()
            link = decrypt_payload(data.get('link_4'), data.get('key'), data.get('iv'))
            
            if link:
                # بدلاً من 302 Redirect، سنقوم بإرسال صفحة HTML بسيطة تشغل الرابط فوراً
                # هذا يضمن أن المشغل والمتصفح يعملان في نفس البيئة
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html_code = f"""
                <html>
                <head>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/shaka-player/4.3.5/shaka-player.compiled.js"></script>
                </head>
                <body style="margin:0; background:#000;">
                    <video id="video" style="width:100%; height:100%;" controls autoplay></video>
                    <script>
                        async function start() {{
                            const video = document.getElementById('video');
                            const player = new shaka.Player(video);
                            player.configure({{
                                drm: {{ clearKeys: {{ 98a5480e7cb53fe7922477f76acba548:ad0076dfd98433a75312bb5e4f14525b }} }} // ضع مفاتيحك هنا
                            }});
                            try {{
                                await player.load('{link}');
                            }} catch (e) {{ console.error(e); }}
                        }}
                        start();
                    </script>
                </body>
                </html>
                """
                self.wfile.write(html_code.encode())
