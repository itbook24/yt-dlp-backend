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
            
            # yt-dlp 2025.06.09-এর জন্য আপডেটেড অপশন
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'ignoreerrors': True,
                'cookiefile': None,
                'nocheckcertificate': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                },
                # ইউটিউবের জন্য বিশেষ 설정
                'extractor_args': {
                    'youtube': {
                        'skip': ['hls', 'dash'],
                        'player_client': ['android', 'web'],
                    }
                },
                # ইউটিউব শর্টস-এর জন্য অতিরিক্ত
                'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                'merge_output_format': 'mp4',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if info is None:
                    return {
                        'success': False,
                        'error': 'Video not found or inaccessible'
                    }
                
                # ভিডিও URL বের করুন
                video_url = None
                if 'url' in info and info['url']:
                    video_url = info['url']
                elif 'formats' in info and info['formats']:
                    # সেরা কোয়ালিটি খুঁজুন
                    for f in info['formats']:
                        if f.get('height') and f.get('height') >= 720:
                            video_url = f['url']
                            break
                    if not video_url and info['formats']:
                        video_url = info['formats'][-1].get('url')
                
                if not video_url:
                    return {
                        'success': False,
                        'error': 'No video URL found'
                    }
                
                return {
                    'success': True,
                    'title': info.get('title', 'Untitled'),
                    'url': video_url,
                    'thumbnail': info.get('thumbnail', ''),
                    'platform': platform,
                    'duration': info.get('duration', 0),
                    'type': 'video'
                }
                
        except Exception as e:
            print(f"❌ Error in get_video_info: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
