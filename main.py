import urllib.request
import urllib.parse
import re
import json

class YouTubeDownloader:
    def __init__(self):
        self.chunk_size = 8192
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

    def extract_video_id(self, url):
        # Handle youtu.be URLs
        if 'youtu.be' in url:
            return url.split('/')[-1].split('?')[0]
        
        # Handle youtube.com URLs
        if 'youtube.com' in url:
            query = urllib.parse.urlparse(url)
            if query.path == '/watch':
                return urllib.parse.parse_qs(query.query)['v'][0]
            elif query.path.startswith('/shorts/'):
                return query.path.split('/')[2]
        return None

    def get_video_info(self, video_id):
        url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        
        player_response = re.search(r'ytInitialPlayerResponse\s*=\s*({.+?})\s*;', html).group(1)
        data = json.loads(player_response)
        
        formats = data['streamingData']['adaptiveFormats']
        audio_formats = [f for f in formats if f['mimeType'].startswith('audio/')]
        best_audio = max(audio_formats, key=lambda x: int(x.get('bitrate', 0)))
        
        return {
            'title': data['videoDetails']['title'],
            'url': best_audio['url']
        }

    def download_audio(self, url, output_path):
        req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
        response = urllib.request.urlopen(req)
        
        with open(output_path, 'wb') as f:
            while True:
                chunk = response.read(self.chunk_size)
                if not chunk:
                    break
                f.write(chunk)

def main():
    downloader = YouTubeDownloader()
    
    print("YouTube to MP3 Converter")
    print("Supported formats: youtube.com/watch, youtu.be, youtube.com/shorts")
    url = input("Enter YouTube URL: ")
    
    video_id = downloader.extract_video_id(url)
    if not video_id:
        print("Invalid YouTube URL")
        return
    
    print("Extracting video info...")
    info = downloader.get_video_info(video_id)
    
    safe_title = "".join(c for c in info['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    output_file = f"{safe_title}.mp3"
    
    print("Downloading audio...")
    downloader.download_audio(info['url'], output_file)
    
    print(f"Done! Saved as: {output_file}")

if __name__ == "__main__":
    main()
