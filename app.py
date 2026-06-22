from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from downloader import VideoDownloader

app = Flask(__name__)
CORS(app, origins='*')
downloader = VideoDownloader()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'ReelGrab API is running'})

@app.route('/api/fetch', methods=['POST'])
def fetch_media():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        url = data['url'].strip()
        if not url:
            return jsonify({'success': False, 'error': 'URL cannot be empty'}), 400
        info = downloader.get_video_info(url)
        if not info or not info.get('success'):
            return jsonify({'success': False, 'error': info.get('error', 'Failed')}), 400
        return jsonify({
            'success': True,
            'data': [{
                'title': info.get('title', 'Untitled'),
                'url': info.get('url', ''),
                'thumbnail': info.get('thumbnail', ''),
                'platform': info.get('platform', 'Unknown'),
                'type': 'video',
            }]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    return jsonify({
        'success': True,
        'platforms': [
            {'name': 'YouTube', 'icon': 'play_circle_fill', 'color': '#FF0000'},
            {'name': 'Instagram', 'icon': 'camera_alt', 'color': '#E4405F'},
            {'name': 'TikTok', 'icon': 'music_note', 'color': '#000000'},
            {'name': 'Facebook', 'icon': 'facebook', 'color': '#1877F2'},
        ]
    })

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    print("🚀 ReelGrab Backend Starting...")
    print("🌐 Server: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)