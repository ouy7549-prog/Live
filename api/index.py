from flask import Flask, redirect
import cloudscraper
import re

app = Flask(__name__)

def get_live_url():
    try:
        scraper = cloudscraper.create_scraper()
        # الرابط الذي يحتوي على مشغل قناة ج
        target_url = "https://www.elahmad.org/tv/radiant.php?id=jscc1"
        headers = {
            "Referer": "https://www.elahmad.org/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = scraper.get(target_url, headers=headers)
        # البحث عن رابط m3u8 داخل كود الصفحة
        match = re.search(r'file:\s*["\'](https?://[^"\']+\.m3u8[^"\']*)["\']', response.text)
        
        if match:
            return match.group(1)
        return None
    except Exception:
        return None

@app.route('/')
@app.route('/play')
def play():
    new_url = get_live_url()
    if new_url:
        # تحويل المشغل مباشرة إلى الرابط الجديد
        return redirect(new_url, code=302)
    return "فشل في استخراج الرابط، جرب مرة أخرى", 500

if __name__ == "__main__":
    app.run()
