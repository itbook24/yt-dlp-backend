@app.route('/api/fetch', methods=['POST'])
def fetch_media():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        url = data['url'].strip()
        if not url:
            return jsonify({'success': False, 'error': 'URL cannot be empty'}), 400
        
        print(f"📥 Fetching: {url}")
        
        # Video info fetch
        info = downloader.get_video_info(url)
        
        # যদি info None অথবা success False হয়
        if not info or not info.get('success'):
            error_msg = info.get('error', 'Failed to fetch video info') if info else 'No response from downloader'
            print(f"❌ Error: {error_msg}")
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # সাফল্য
        return jsonify({
            'success': True,
            'data': [{
                'title': info.get('title', 'Untitled'),
                'url': info.get('url', ''),
                'thumbnail': info.get('thumbnail', ''),
                'platform': info.get('platform', 'Unknown'),
                'type': 'video',
                'duration': info.get('duration', 0)
            }]
        })
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
