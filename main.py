from flask import Flask, render_template, request, send_file
import urllib.request
import urllib.parse
import re
import json
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

class YouTubeDownloader:
    def __init__(self):
        self.chunk_size = 8192
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

    def extract_video_id(self, url):
        """Extracts YouTube video ID from the given URL."""
        if 'youtu.be' in url:
            return url.split('/')[-1].split('?')[0]
        
        if 'youtube.com' in url:
            query = urllib.parse.urlparse(url)
            if query.path == '/watch':
                return urllib.parse.parse_qs(query.query).get('v', [None])[0]
            elif query.path.startswith('/shorts/'):
                return query.path.split('/')[2]
        return None

    def get_video_info(self, video_id):
        """Fetches video information and the best audio URL."""
        url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        
        player_response = re.search(r'ytInitialPlayerResponse\s*=\s*({.+?})\s*;', html)
        if not player_response:
            raise ValueError("Could not find video information.")
        
        data = json.loads(player_response.group(1))
        formats = data['streamingData']['adaptiveFormats']
        audio_formats = [f for f in formats if f['mimeType'].startswith('audio/')]
        
        if not audio_formats:
            raise ValueError("No audio formats available.")
        
        best_audio = max(audio_formats, key=lambda x: int(x.get('bitrate', 0)))
        return {
            'title': data['videoDetails']['title'],
            'url': best_audio['url']
        }

    def download_audio(self, url, output_path):
        """Downloads audio from the given URL and saves it to the specified path."""
        req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
        response = urllib.request.urlopen(req)
        
        with open(output_path, 'wb') as f:
            while chunk := response.read(self.chunk_size):
                f.write(chunk)

@app.route('/', methods=['GET', 'POST'])
def home():
    """Handles the home route for the application."""
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return render_template('index.html', error="Please enter a URL")

        downloader = YouTubeDownloader()
        video_id = downloader.extract_video_id(url)
        
        if not video_id:
            return render_template('index.html', error="Invalid YouTube URL")

        try:
            info = downloader.get_video_info(video_id)
            safe_title = "".join(c for c in info['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_file = os.path.join(DOWNLOAD_FOLDER, f"{safe_title}.mp3")
            
            downloader.download_audio(info['url'], output_file)
            
            return send_file(
                output_file,
                as_attachment=True,
                download_name=f"{safe_title}.mp3"
            )
        except Exception as e:
            return render_template('index.html', error=f"Download failed: {str(e)}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
