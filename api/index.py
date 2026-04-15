from flask import Flask, redirect
import cloudscraper
import re

app = Flask(__name__)

def get_jeem_url():
    scraper = cloudscraper.create_scraper()
    # 1. الدخول لصفحة القناة الرئيسية لجلب الكوكيز والتوكن
    base_url = "https://www.elahmad.org/tv/radiant.php?id=jscc1"
    headers = {
        "Referer": "https://www.elahmad.org/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = scraper.get(base_url, headers=headers)
        
        # 2. البحث عن التوكن (غالباً يكون نصاً طويلاً في كود الصفحة)
        # سنبحث عن أي رابط m3u8 يظهر في الصفحة
        match = re.search(r'["\'](https?://games1\.elahmad\.xyz/[^"\']+\.m3u8[^"\']*)["\']', response.text)
        
        if match:
            return match.group(1).replace('\\', '')
        
        # 3. محاولة أخيرة: إذا لم يجد الرابط كاملاً، سيبحث عن التوكن فقط لتركيبه
        token_match = re.search(r'token=([a-zA-Z0-9\-_]+)', response.text)
        if token_match:
            token = token_match.group(1)
            # تركيب الرابط بناءً على الصيغة التي أرسلتها سابقاً
            return f"https://games1.elahmad.xyz/tv793_www.elahmad.com_jeem/index.m3u8?token={token}"

    except Exception:
        pass
    return None

@app.route('/')
def play():
    url = get_jeem_url()
    if url:
        return redirect(url, code=302)
    
    # إذا فشل السيرفر، سنعطيك رابطاً احتياطياً (قد يعمل أو لا حسب التوكن)
    return "السيرفر لم يستطع جلب توكن جديد حالياً. حاول تحديث الصفحة بعد ثوانٍ.", 500
