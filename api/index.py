from flask import Flask, render_template_string

app = Flask(__name__)

# --- ضع بياناتك هنا ---
# تأكد أن الرابط يبدأ بـ https:// والمفاتيح بصيغة Hex (أرقام وحروف بدون : أو مسافات)
STREAM_URL = "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-2/51db9d7fa48a27d051f1eecb68069151/index.mpd"
KID_HEX = "e3ce77324a3d4fa2a913b26cc1976052"
KEY_HEX = "17774f82a3b9e33ea7a149596acbb20f"
# ----------------------

@app.route('/')
@app.route('/api')
def index():
    html_template = """
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gemini Live Player</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/shaka-player/4.3.5/shaka-player.compiled.js"></script>
        <style>
            body { margin: 0; background-color: #000; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
            #video-container { width: 100%; height: 100%; max-width: 1200px; aspect-ratio: 16/9; }
            video { width: 100%; height: 100%; outline: none; }
        </style>
    </head>
    <body>
        <div id="video-container">
            <video id="video" controls autoplay playsinline></video>
        </div>

        <script>
            async function initPlayer() {
                const video = document.getElementById('video');
                const player = new shaka.Player(video);

                // إعداد فك التشفير باستخدام ClearKey
                player.configure({
                    drm: {
                        clearKeys: {
                            '{{ kid }}': '{{ key }}'
                        }
                    }
                });

                // معالجة أخطاء المشغل
                player.addEventListener('error', (event) => {
                    console.error('Error code', event.detail.code, 'object', event.detail);
                });

                try {
                    await player
