import requests
import re

def get_starz_token():
    # رابط القناة
    url = "https://starzplay.com/ar/watch/movies/national-geographic-abu-dhabi/720335400128"
    
    # الـ Headers هنا هي السر لإيقاف التوجيه للرئيسية
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
        'Referer': 'https://starzplay.com/ar/',
        'Origin': 'https://starzplay.com'
    }
    
    # استخدام Session للحفاظ على الكوكيز أثناء الطلب
    session = requests.Session()
    
    try:
        # الدخول أولاً للرئيسية لجلب كوكيز البداية
        session.get("https://starzplay.com/ar/", headers=headers, timeout=10)
        
        # الآن محاولة الدخول لرابط القناة
        response = session.get(url, headers=headers, timeout=10)
        
        # البحث عن التوكن داخل الكود
        token_match = re.search(r'token:\s*"(.*?)"', response.text)
        if token_match:
            return token_match.group(1)
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
