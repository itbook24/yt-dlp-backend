import yt_dlp
import os

class VideoDownloader:
    def __init__(self):
        self.download_folder = 'downloads'
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
    
    def get_platform(self, url):
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'YouTube'
        elif 'instagram.com' in url:
            return 'Instagram'
        elif 'tiktok.com' in url:
            return 'TikTok'
        elif 'facebook.com' in url or 'fb.com' in url:
            return 'Facebook'
        return 'Unknown'
    
    def get_video_info(self, url):
        try:
            platform = self.get_platform(url)
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'ignoreerrors': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info is None:
                    return None
                video_url = None
                if 'url' in info:
                    video_url = info['url']
                elif 'formats' in info and info['formats']:
                    for f in info['formats']:
                        if f.get('height') and f.get('height') >= 720:
                            video_url = f['url']
                            break
                    if not video_url:
                        video_url = info['formats'][-1]['url']
                return {
                    'success': True,
                    'title': info.get('title', 'Untitled'),
                    'url': video_url,
                    'thumbnail': info.get('thumbnail', ''),
                    'platform': platform,
                    'duration': info.get('duration', 0),
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}