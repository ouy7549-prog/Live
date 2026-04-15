from flask import Flask, redirect
import cloudscraper
import re

app = Flask(__name__)

def get_jeem_stream():
    # استخدام سكرابر متطور لتجاوز الحماية
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    
    # الرابط المباشر للمشغل
    target_url = "https://www.elahmad.org/tv/radiant.php?id=jscc1"
    
    headers = {
        "Referer": "https://www.elahmad.org/tv/aljazeera_children.php",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ar,en-US;q=0.7,en;q=0.3",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        # 1. جلب الصفحة
        resp = scraper.get(target_url, headers=headers, timeout=10)
        
        # 2. البحث عن الرابط باستخدام Regex يدعم الروابط المكسورة أو المشفرة جزئياً
        # نبحث عن نمط: https://...index.m3u8?token=...
        content = resp.text
        
        # محاولة البحث عن الرابط الكامل
        patterns = [
            r'(https?://[^\s"\']+\.m3u8[^\s"\']*)',
            r'file\s*:\s*["\']([^"\']+)["\']',
            r'src\s*:\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for link in matches:
                if 'elahmad' in link and 'm3u8' in link:
                    # تنظيف الرابط من الهروب (Backslashes)
                    clean_link = link.replace('\\', '')
                    return clean_link
        
        return None
    except Exception as e:
        print(f"Detailed Error: {e}")
        return None

@app.route('/')
@app.route('/api')
def get_stream():
    link = get_jeem_stream()
    if link:
        return redirect(link, code=302)
    
    return "Error: Link not found. The site might be blocking the Cloud Server IP.", 500

if __name__ == "__main__":
    app.run()
