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
        import logging
        logger = logging.getLogger(__name__)
        
        # Extract channel ID from URL if needed
        channel_id = self._extract_channel_id(channel_id)
        logger.info(f"[YouTube] Getting videos for channel: {channel_id}")
        
        # First get the uploads playlist ID
        params = {
            'part': 'contentDetails',
            'id': channel_id
        }
        
        try:
            data = self._make_request('channels', params)
        except Exception as e:
            logger.error(f"[YouTube] Failed to get channel info: {str(e)}")
            raise
        
        items = data.get('items', [])
        logger.info(f"[YouTube] Found {len(items)} channel items")
        
        if not items:
            logger.error(f"[YouTube] Channel not found: {channel_id}")
            raise YouTubeAPIError(f'Channel not found: {channel_id}')
        
        uploads_playlist = items[0].get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')
        logger.info(f"[YouTube] Uploads playlist ID: {uploads_playlist}")
        
        if not uploads_playlist:
            logger.error(f"[YouTube] No uploads playlist found")
            return []
        
        # Get videos from uploads playlist
        params = {
            'part': 'snippet',
            'playlistId': uploads_playlist,
            'maxResults': max_results
        }
        
        logger.info(f"[YouTube] Fetching playlist items...")
        data = self._make_request('playlistItems', params)
        video_ids = [item['snippet']['resourceId']['videoId'] for item in data.get('items', [])]
        logger.info(f"[YouTube] Found {len(video_ids)} video IDs")
        
        videos = self.get_video_details(video_ids)
        logger.info(f"[YouTube] Retrieved details for {len(videos)} videos")
        return videos
    
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
    
    def _extract_channel_id(self, input_str: str) -> str:
        """Extract channel ID from URL or handle @username."""
        import logging
        import re
        logger = logging.getLogger(__name__)
        
        logger.info(f"[YouTube] Extracting channel ID from: {input_str}")
        
        # If already a channel ID (starts with UC)
        if input_str.startswith('UC') and len(input_str) == 24:
            logger.info(f"[YouTube] Already a channel ID: {input_str}")
            return input_str
        
        # Extract from URL patterns
        patterns = [
            r'youtube\.com/channel/([^/?&]+)',
            r'youtube\.com/c/([^/?&]+)',
            r'youtube\.com/@([^/?&]+)',
            r'youtube\.com/user/([^/?&]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, input_str)
            if match:
                identifier = match.group(1)
                logger.info(f"[YouTube] Extracted identifier: {identifier}")
                
                # If it's @username or custom URL, need to resolve it
                if not identifier.startswith('UC'):
                    resolved = self._resolve_channel_id(identifier)
                    if resolved:
                        return resolved
                return identifier
        
        # If it's just @username without URL
        if input_str.startswith('@'):
            username = input_str[1:]
            logger.info(f"[YouTube] Resolving @username: {username}")
            resolved = self._resolve_channel_id(username)
            if resolved:
                return resolved
        
        # Try as-is (might be username or custom URL)
        logger.info(f"[YouTube] Trying to resolve as username: {input_str}")
        resolved = self._resolve_channel_id(input_str)
        if resolved:
            return resolved
        
        logger.warning(f"[YouTube] Could not extract channel ID, using as-is: {input_str}")
        return input_str
    
    def _resolve_channel_id(self, username: str) -> str:
        """Resolve username/handle to channel ID using search."""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"[YouTube] Searching for channel: {username}")
            params = {
                'part': 'snippet',
                'q': username,
                'type': 'channel',
                'maxResults': 1
            }
            
            data = self._make_request('search', params)
            items = data.get('items', [])
            
            if items:
                channel_id = items[0]['snippet']['channelId']
                logger.info(f"[YouTube] Resolved to channel ID: {channel_id}")
                return channel_id
            
            logger.warning(f"[YouTube] No channel found for: {username}")
            return None
        except Exception as e:
            logger.error(f"[YouTube] Error resolving channel: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        return bool(api_key_manager.get_active_key('youtube'))

youtube_client = YouTubeClient()
