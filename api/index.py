from http.server import BaseHTTPRequestHandler
import cloudscraper
import re

def get_live_link():
    """دالة تجلب الرابط المباشر لقناة ج من موقع الأحمد"""
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
    )
    
    # رابط الصفحة التي تحتوي على مشغل القناة
    url = "https://www.elahmad.org/tv/radiant.php?id=jscc1"
    headers = {
        "Referer": "https://www.elahmad.org/tv/aljazeera_children.php",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        resp = scraper.get(url, headers=headers, timeout=10)
        # البحث عن أي رابط ينتهي بـ m3u8 ويحتوي على التوكن
        match = re.search(r'["\'](https?://[^"\']+\.m3u8[^"\']*)["\']', resp.text)
        if match:
            return match.group(1).replace('\\', '')
        return None
    except:
        return None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # محاولة جلب الرابط المباشر
        link = get_live_link()
        
        if link:
            # إرسال استجابة 302 (تحويل مؤقت) للمشغل
            self.send_response(302)
            self.send_header('Location', link)
            self.send_header('Access-Control-Allow-Origin', '*') # لحل مشاكل CORS
            self.end_headers()
        else:
            # في حال الفشل
            self.send_response(500)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("خطأ: لم يتم العثور على رابط البث. قد تكون الحماية قد تغيرت.".encode('utf-8'))

# ملاحظة: إذا كنت تريد العودة لفك تشفير AES لقنوات مثل دبي وان، 
# يمكنك دمج دالة decrypt_payload هنا واستدعاؤها بنفس الطريقة.
