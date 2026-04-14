from flask import Flask, render_template_string

app = Flask(__name__)

# --- بياناتك ---
STREAM_URL = "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-2/51db9d7fa48a27d051f1eecb68069151/index.mpd"
KID_HEX = "e3ce77324a3d4fa2a913b26cc1976052"
KEY_HEX = "17774f82a3b9e33ea7a149596acbb20f"

@app.route('/')
def home():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Stream</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/shaka-player/4.3.5/shaka-player.compiled.js"></script>
        <style>body { margin: 0; background: #000; }</style>
    </head>
    <body>
        <video id="video" style="width:100vw; height:100vh;" controls autoplay></video>
        <script>
            async function init() {
                const video = document.getElementById('video');
                const player = new shaka.Player(video);
                player.configure({
                    drm: { clearKeys: { '{{ kid }}': '{{ key }}' } }
                });
                try { await player.load('{{ url }}'); } catch (e) { console.error(e); }
            }
            document.addEventListener('DOMContentLoaded', init);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, url=STREAM_URL, kid=KID_HEX, key=KEY_HEX)

# مهم جداً لـ Vercel
app.debug = True
