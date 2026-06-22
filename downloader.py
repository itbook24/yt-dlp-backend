import yt_dlp
import os
import re

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
            
            # yt-dlp অপশন (সর্বশেষ ভার্সনের জন্য)
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
                # ইউটিউবের জন্য বিশেষ এক্সট্র্যাক্টর
                'extractor_args': {
                    'youtube': {
                        'skip': ['hls', 'dash'],
                        'player_client': ['android', 'web'],
                    }
                },
                # সেরা কোয়ালিটি
                'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                'merge_output_format': 'mp4',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # যদি info None হয়
                if info is None:
                    return {
                        'success': False,
                        'error': 'Video not found or inaccessible'
                    }
                
                # ভিডিও URL বের করুন
                video_url = None
                
                # সরাসরি URL থাকলে
                if 'url' in info and info['url']:
                    video_url = info['url']
                # ফরম্যাট থেকে বের করুন
                elif 'formats' in info and info['formats']:
                    # প্রথমে 720p বা তার বেশি খুঁজুন
                    for f in info['formats']:
                        if f.get('height') and f.get('height') >= 720:
                            video_url = f.get('url')
                            break
                    # না পেলে সেরা ফরম্যাট নিন
                    if not video_url and info['formats']:
                        video_url = info['formats'][-1].get('url')
                
                # এখনও URL না পেলে Error
                if not video_url:
                    return {
                        'success': False,
                        'error': 'No video URL found'
                    }
                
                # সাফল্য
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
