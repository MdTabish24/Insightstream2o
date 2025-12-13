import requests
from datetime import datetime, timezone
from django.conf import settings
from django.core.cache import cache
from core.utils.api_key_manager import api_key_manager
from core.utils.retry import retry_with_backoff
from core.exceptions import YouTubeAPIError, RateLimitExceeded

class YouTubeClient:
    BASE_URL = "https://www.googleapis.com/youtube/v3"
    CACHE_TIMEOUT = 300  # 5 minutes
    
    def _get_api_key(self) -> str:
        key = api_key_manager.get_active_key('youtube')
        if not key:
            raise YouTubeAPIError('No YouTube API key available')
        return key
    
    def _make_request(self, endpoint: str, params: dict) -> dict:
        params['key'] = self._get_api_key()
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 403:
                if 'quotaExceeded' in response.text:
                    api_key_manager.rotate_key('youtube')
                    if api_key_manager.is_exhausted('youtube'):
                        raise RateLimitExceeded('YouTube API quota exceeded')
                    return self._make_request(endpoint, params)
                raise YouTubeAPIError('YouTube API access forbidden')
            
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            raise YouTubeAPIError(f'YouTube API error: {str(e)}')
    
    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def search_videos(self, query: str, max_results: int = 10) -> list:
        """Search for videos by query."""
        cache_key = f'yt_search_{query}_{max_results}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': max_results
        }
        
        data = self._make_request('search', params)
        video_ids = [item['id']['videoId'] for item in data.get('items', [])]
        
        if not video_ids:
            return []
        
        # Get statistics for videos
        videos = self.get_video_details(video_ids)
        cache.set(cache_key, videos, self.CACHE_TIMEOUT)
        return videos
    
    def get_video_details(self, video_ids: list) -> list:
        """Get detailed info for videos including statistics."""
        if not video_ids:
            return []
        
        params = {
            'part': 'snippet,statistics,contentDetails',
            'id': ','.join(video_ids)
        }
        
        data = self._make_request('videos', params)
        videos = []
        
        for item in data.get('items', []):
            snippet = item.get('snippet', {})
            stats = item.get('statistics', {})
            content = item.get('contentDetails', {})
            
            videos.append({
                'id': item['id'],
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                'channel_title': snippet.get('channelTitle', ''),
                'channel_id': snippet.get('channelId', ''),
                'publish_date': snippet.get('publishedAt', ''),
                'views': int(stats.get('viewCount', 0)),
                'likes': int(stats.get('likeCount', 0)),
                'comments': int(stats.get('commentCount', 0)),
                'duration': content.get('duration', ''),
            })
        
        return videos
    
    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> list:
        """Get videos from a channel's uploads playlist."""
        # First get the uploads playlist ID
        params = {
            'part': 'contentDetails',
            'id': channel_id
        }
        
        data = self._make_request('channels', params)
        items = data.get('items', [])
        
        if not items:
            raise YouTubeAPIError(f'Channel not found: {channel_id}')
        
        uploads_playlist = items[0].get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')
        
        if not uploads_playlist:
            return []
        
        # Get videos from uploads playlist
        params = {
            'part': 'snippet',
            'playlistId': uploads_playlist,
            'maxResults': max_results
        }
        
        data = self._make_request('playlistItems', params)
        video_ids = [item['snippet']['resourceId']['videoId'] for item in data.get('items', [])]
        
        return self.get_video_details(video_ids)
    
    def get_trending_videos(self, region_code: str = 'US', max_results: int = 20) -> list:
        """Get trending videos."""
        cache_key = f'yt_trending_{region_code}_{max_results}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        params = {
            'part': 'snippet,statistics',
            'chart': 'mostPopular',
            'regionCode': region_code,
            'maxResults': max_results
        }
        
        data = self._make_request('videos', params)
        videos = []
        
        for item in data.get('items', []):
            snippet = item.get('snippet', {})
            stats = item.get('statistics', {})
            
            videos.append({
                'id': item['id'],
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                'channel_title': snippet.get('channelTitle', ''),
                'views': int(stats.get('viewCount', 0)),
                'likes': int(stats.get('likeCount', 0)),
            })
        
        cache.set(cache_key, videos, self.CACHE_TIMEOUT)
        return videos
    
    def is_available(self) -> bool:
        return bool(api_key_manager.get_active_key('youtube'))

youtube_client = YouTubeClient()
