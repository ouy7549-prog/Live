import requests
import re

def get_starz_token():
    # محاولة جلب التوكن من رابط مباشر أكثر استجابة للسكربتات
    url = "https://starzplay.com/ar/watch/movies/national-geographic-abu-dhabi/720335400128"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'ar'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        match = re.search(r'token:\s*"(.*?)"', response.text)
        return match.group(1) if match else None
    except:
        return None

token = get_starz_token()
# إذا فشل GitHub في جلب التوكن، سنضع توكن "افتراضي" مؤقت للتجربة
final_token = token if token else "TOKEN_EXPIRED_RE-RUN_ACTION"

m3u_content = f"""#EXTM3U
#EXTINF:-1, National Geographic
#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha
#KODIPROP:inputstream.adaptive.license_key=https://widevine-license.vudrm.tech/proxy|x-vudrm-token={final_token}&User-Agent=Mozilla/5.0
https://admn-live-cdn-lb.starzplayarabia.com/out/v1/admn_tv_enc/national_geo/national_geo_dash/index.mpd"""

with open("index.html", "w") as f: # سنحفظه كـ index ليعمل كرابط مباشر
    f.write(m3u_content)
