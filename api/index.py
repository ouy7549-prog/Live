from flask import Flask, render_template_string

app = Flask(__name__)

# --- بياناتك هنا ---
MPD_URL = "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-2/51db9d7fa48a27d051f1eecb68069151/index.mpd
"
KEY_ID = "e3ce77324a3d4fa2a913b26cc1976052"
KEY_VALUE = "17774f82a3b9e33ea7a149596acbb20f"
# ------------------

@app.route('/')
@app.route('/api')
def home():
    # كود HTML لمشغل متطور يدعم DRM
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Stream</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/shaka-player/4.3.5/shaka-player.compiled.js"></script>
        <style>
            body { margin: 0; background: #000; overflow: hidden; }
            #video { width: 100vw; height: 100vh; background: #000; }
        </style>
    </head>
    <body>
        <video id="video" controls autoplay></video>
        <script>
            async function initPlayer() {
                const video = document.getElementById('video');
                const player = new shaka.Player(video);

                // إعداد المفاتيح لفك التشفير تلقائياً
                player.configure({
                    drm: {
                        clearKeys: {
                            '{{ key_id }}': '{{ key_value }}'
                        }
                    }
                });

                try {
                    await player.load('{{ mpd_url }}');
                    console.log('Stream loaded successfully!');
                } catch (e) {
                    console.error('Error loading stream:', e);
                }
            }
            document.addEventListener('DOMContentLoaded', initPlayer);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, 
                                 mpd_url=MPD_URL, 
                                 key_id=KEY_ID, 
                                 key_value=KEY_VALUE)
