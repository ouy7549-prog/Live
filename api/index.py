from flask import Flask, redirect
import cloudscraper
import re

app = Flask(__name__)

def get_live_url():
    try:
        # استخدام cloudscraper لتجاوز حماية Cloudflare
        scraper = cloudscraper.create_scraper()
        
        # الرابط الذي يحتوي على مشغل قناة ج
        target_url = "https://www.elahmad.org/tv/radiant.php?id=jscc1"
        headers = {
            "Referer": "https://www.elahmad.org/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        
        response = scraper.get(target_url, headers=headers)
        
        # محاولة البحث عن الرابط بأكثر من نمط (Pattern)
        # النمط 1: البحث عن روابط m3u8 داخل ملفات JS
        patterns = [
            r'["\'](https?://[^"\']+\.m3u8[^"\']*)["\']',
            r'file\s*:\s*["\']([^"\']+)["\']',
            r'src\s*:\s*["\']([^"\']+\.m3u8[^"\']*)["\']'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                link = match.group(1)
                # التأكد من أن الرابط يبدأ بـ http
                if not link.startswith('http'):
                    continue
                return link
                
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def play():
    new_url = get_live_url()
    if new_url:
        # إرجاع الرابط كـ Redirect (هذا ما يحتاجه المشغل)
        return redirect(new_url, code=302)
    
    # في حال الفشل، سنحاول طباعة جزء من كود الصفحة للتشخيص (اختياري)
    return "فشل في استخراج الرابط، ربما تغيرت بنية الصفحة. جرب التحديث.", 500

if __name__ == "__main__":
    app.run()
