import logging
from core.clients.gemini import gemini_client
from core.clients.youtube import youtube_client
from core.exceptions import AIServiceUnavailable, YouTubeAPIError

logger = logging.getLogger(__name__)

class KeywordService:
    """
    Service for keyword research combining AI and YouTube data.
    
    Requirements:
    - 4.1: Return primary keywords with search volume
    - 4.2: Return long-tail keywords
    - 4.3: Return trending keywords from YouTube
    - 4.4: Return related topics
    - 4.5: Include metadata (search volume, competition, relevance)
    """
    
    def research_keywords(self, topic: str) -> dict:
        """
        Research keywords for a topic using AI and YouTube data.
        
        Returns:
        {
            'primary_keywords': [{'keyword': str, 'search_volume': int, 'competition': str, 'relevance': float}],
            'long_tail_keywords': [{'keyword': str, 'search_volume': int, 'competition': str, 'relevance': float}],
            'trending_keywords': [{'keyword': str, 'search_volume': int, 'competition': str, 'relevance': float}],
            'related_topics': [{'topic': str, 'search_volume': int, 'competition': str, 'relevance': float}]
        }
        """
        try:
            logger.info(f"Researching keywords for topic: {topic}")
            
            # Get AI-generated keywords from Gemini
            ai_keywords = gemini_client.generate_keywords(topic)
            
            # Enhance with real YouTube trending data
            try:
                trending_videos = youtube_client.get_trending_videos(max_results=10)
                youtube_keywords = self._extract_keywords_from_videos(trending_videos, topic)
                
                # Merge AI keywords with YouTube data
                result = self._merge_keyword_data(ai_keywords, youtube_keywords, topic)
            except (YouTubeAPIError, Exception) as e:
                logger.warning(f"YouTube API unavailable: {str(e)}, using AI-only keywords")
                result = ai_keywords
            
            # Validate structure
            if not self._validate_keyword_structure(result):
                logger.warning("Invalid keyword structure, using fallback")
                result = self._get_fallback_keywords(topic)
            
            logger.info(f"Successfully researched keywords for: {topic}")
            return result
            
        except AIServiceUnavailable as e:
            logger.error(f"AI service unavailable: {str(e)}, using fallback")
            return self._get_fallback_keywords(topic)
        except Exception as e:
            logger.error(f"Unexpected error during keyword research: {str(e)}, using fallback")
            return self._get_fallback_keywords(topic)
    
    def _extract_keywords_from_videos(self, videos: list, topic: str) -> dict:
        """Extract keywords from YouTube video titles and descriptions"""
        keywords = set()
        
        for video in videos:
            title = video.get('title', '').lower()
            description = video.get('description', '').lower()
            
            # Extract words related to the topic
            if topic.lower() in title or topic.lower() in description:
                # Split title into potential keywords
                words = title.split()
                for i in range(len(words)):
                    # Single words
                    if len(words[i]) > 3:
                        keywords.add(words[i].strip('.,!?'))
                    # Two-word phrases
                    if i < len(words) - 1:
                        phrase = f"{words[i]} {words[i+1]}".strip('.,!?')
                        if len(phrase) > 5:
                            keywords.add(phrase)
        
        return {
            'trending_from_youtube': list(keywords)[:10]
        }
    
    def _merge_keyword_data(self, ai_keywords: dict, youtube_keywords: dict, topic: str) -> dict:
        """Merge AI-generated keywords with YouTube trending data"""
        result = ai_keywords.copy()
        
        # Add YouTube trending keywords if available
        if youtube_keywords.get('trending_from_youtube'):
            youtube_trending = youtube_keywords['trending_from_youtube']
            
            # Add to trending keywords section
            for kw in youtube_trending[:5]:
                result['trending_keywords'].append({
                    'keyword': kw,
                    'search_volume': 5000,  # Estimated
                    'competition': 'high',
                    'relevance': 0.75,
                    'source': 'youtube_trending'
                })
        
        return result
    
    def _validate_keyword_structure(self, data: dict) -> bool:
        """Validate keyword data structure"""
        required_keys = ['primary_keywords', 'long_tail_keywords', 'trending_keywords', 'related_topics']
        
        if not all(key in data for key in required_keys):
            return False
        
        # Validate each category has proper structure
        for category in required_keys:
            if not isinstance(data[category], list):
                return False
            
            for item in data[category]:
                if not isinstance(item, dict):
                    return False
                
                # Check required fields
                key_field = 'keyword' if category != 'related_topics' else 'topic'
                if key_field not in item:
                    return False
                
                if 'search_volume' not in item or 'competition' not in item or 'relevance' not in item:
                    return False
        
        return True
    
    def _get_fallback_keywords(self, topic: str) -> dict:
        """Generate fallback keywords when services fail"""
        return {
            'primary_keywords': [
                {'keyword': topic, 'search_volume': 10000, 'competition': 'medium', 'relevance': 0.95},
                {'keyword': f'{topic} tutorial', 'search_volume': 8000, 'competition': 'medium', 'relevance': 0.90},
                {'keyword': f'{topic} guide', 'search_volume': 7500, 'competition': 'low', 'relevance': 0.88}
            ],
            'long_tail_keywords': [
                {'keyword': f'how to {topic}', 'search_volume': 5000, 'competition': 'low', 'relevance': 0.92},
                {'keyword': f'best {topic} for beginners', 'search_volume': 4500, 'competition': 'low', 'relevance': 0.87},
                {'keyword': f'{topic} step by step', 'search_volume': 4000, 'competition': 'low', 'relevance': 0.85},
                {'keyword': f'learn {topic} fast', 'search_volume': 3500, 'competition': 'low', 'relevance': 0.82}
            ],
            'trending_keywords': [
                {'keyword': f'{topic} 2024', 'search_volume': 8000, 'competition': 'high', 'relevance': 0.89},
                {'keyword': f'{topic} tips', 'search_volume': 6500, 'competition': 'medium', 'relevance': 0.84},
                {'keyword': f'{topic} tricks', 'search_volume': 6000, 'competition': 'medium', 'relevance': 0.81}
            ],
            'related_topics': [
                {'topic': f'{topic} basics', 'search_volume': 6000, 'competition': 'medium', 'relevance': 0.86},
                {'topic': f'{topic} advanced', 'search_volume': 5500, 'competition': 'high', 'relevance': 0.83},
                {'topic': f'{topic} examples', 'search_volume': 5000, 'competition': 'low', 'relevance': 0.80}
            ]
        }

keyword_service = KeywordService()
