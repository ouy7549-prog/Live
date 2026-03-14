import requests
import re

def get_starz_token():
    # هذا الرابط يحاول الوصول لبيانات الفيديو مباشرة
    url = "https://starzplay.com/ar/watch/movies/national-geographic-abu-dhabi/720335400128"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://starzplay.com/ar/',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        session = requests.Session()
        # زيارة الرئيسية أولاً لإنشاء جلسة
        session.get("https://starzplay.com/ar/", headers=headers)
        # طلب صفحة القناة
        response = session.get(url, headers=headers)
        
        # محاولة البحث عن التوكن
        token = re.search(r'token:\s*"(.*?)"', response.text)
        if token:
            return token.group(1)
        return None
    except:
        return None
