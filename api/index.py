from flask import Flask, redirect
import cloudscraper
import re

app = Flask(__name__)

def get_jeem_stream():
    scraper = cloudscraper.create_scraper()
    # الرابط الجديد لقناة ج
    target_url = "https://www.elahmad.org/tv/radiant.php?id=jscc1"
    headers = {
        "Referer": "https://www.elahmad.org/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        # جلب محتوى الصفحة
        resp = scraper.get(target_url, headers=headers)
        
        # البحث عن رابط m3u8 الذي يحتوي على التوكن
        # قناة ج لا تحتاج فك تشفير AES، الرابط موجود نصياً في الكود
        found = re.findall(r'file\s*:\s*["\'](https?://[^"\']+\.m3u8[^"\']*)["\']', resp.text)
        
        if found:
            link = found[0].replace('\\', '')
            # تنظيف الرابط من أي رموز غريبة
            clean_link = "".join(char for char in link if 31 < ord(char) < 127)
            return clean_link
        
        # محاولة أخرى ببحث أعمق
        found_alt = re.search(r'["\'](https?://games1\.elahmad\.xyz/[^"\']+)["\']', resp.text)
        if found_alt:
            return found_alt.group(1).replace('\\', '')
            
        return None
    except:
        return None

@app.route('/')
@app.route('/api')
def get_stream():
    link = get_jeem_stream()
    
    if link:
        # تحويل المشغل (VLC/OTT) للرابط الجديد فوراً
        return redirect(link, code=302)
    
    return "Error: JeemTV link not found. The site might have changed the structure.", 500

# إعدادات Vercel
app.debug = True
