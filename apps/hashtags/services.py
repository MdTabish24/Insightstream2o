import re
import logging
from collections import Counter
from core.clients.youtube import youtube_client
from core.clients.gemini import gemini_client
from core.exceptions import YouTubeAPIError, AIServiceUnavailable

logger = logging.getLogger(__name__)

class HashtagService:
    def extract_hashtags(self, text: str) -> list:
        """Extract hashtags from text using regex pattern."""
        return re.findall(r'#[a-zA-Z0-9_]+', text)
    
    def generate_hashtags(self, topic: str) -> dict:
        """Generate hashtags combining real YouTube data and AI suggestions."""
        try:
            # Extract real hashtags from trending videos
            real_hashtags = self._extract_from_trending(topic)
            
            # Generate AI hashtags
            ai_hashtags = self._generate_ai_hashtags(topic)
            
            # Combine and deduplicate
            combined = self._combine_hashtags(real_hashtags, ai_hashtags)
            
            return {
                'real_hashtags': real_hashtags[:10],
                'ai_hashtags': ai_hashtags[:10],
                'combined': combined[:15]
            }
        except Exception as e:
            logger.error(f'Hashtag generation error: {str(e)}')
            return self._fallback_hashtags(topic)
    
    def _extract_from_trending(self, topic: str) -> list:
        """Extract hashtags from trending YouTube videos."""
        try:
            # Get trending videos
            videos = youtube_client.get_trending_videos(max_results=20)
            
            # Extract hashtags from descriptions
            all_hashtags = []
            for video in videos:
                description = video.get('description', '')
                hashtags = self.extract_hashtags(description)
                all_hashtags.extend(hashtags)
            
            # Count occurrences
            hashtag_counts = Counter(all_hashtags)
            
            # Format with engagement metrics
            result = []
            for hashtag, count in hashtag_counts.most_common(15):
                engagement = 'high' if count >= 5 else 'medium' if count >= 3 else 'low'
                result.append({
                    'hashtag': hashtag,
                    'usage_count': count,
                    'engagement': engagement
                })
            
            return result
        except YouTubeAPIError as e:
            logger.warning(f'YouTube API error in hashtag extraction: {str(e)}')
            return []
    
    def _generate_ai_hashtags(self, topic: str) -> list:
        """Generate hashtags using Gemini AI."""
        try:
            hashtags = gemini_client.generate_hashtags(topic)
            
            # Format with estimated metrics
            result = []
            for i, hashtag in enumerate(hashtags[:10]):
                # Ensure hashtag starts with #
                if not hashtag.startswith('#'):
                    hashtag = f'#{hashtag}'
                
                # Estimate usage based on position
                usage = 1000 - (i * 100)
                engagement = 'high' if i < 3 else 'medium' if i < 7 else 'low'
                
                result.append({
                    'hashtag': hashtag,
                    'usage_count': usage,
                    'engagement': engagement
                })
            
            return result
        except AIServiceUnavailable as e:
            logger.warning(f'AI service error in hashtag generation: {str(e)}')
            return []
    
    def _combine_hashtags(self, real: list, ai: list) -> list:
        """Combine real and AI hashtags, removing duplicates."""
        seen = set()
        combined = []
        
        # Prioritize real hashtags
        for item in real:
            hashtag = item['hashtag'].lower()
            if hashtag not in seen:
                seen.add(hashtag)
                combined.append(item['hashtag'])
        
        # Add AI hashtags
        for item in ai:
            hashtag = item['hashtag'].lower()
            if hashtag not in seen:
                seen.add(hashtag)
                combined.append(item['hashtag'])
        
        return combined
    
    def _fallback_hashtags(self, topic: str) -> dict:
        """Fallback hashtags if all services fail."""
        topic_clean = topic.replace(' ', '').lower()
        fallback = [
            {'hashtag': f'#{topic_clean}', 'usage_count': 1000, 'engagement': 'high'},
            {'hashtag': '#youtube', 'usage_count': 5000, 'engagement': 'high'},
            {'hashtag': '#viral', 'usage_count': 3000, 'engagement': 'high'},
            {'hashtag': '#trending', 'usage_count': 2500, 'engagement': 'medium'},
            {'hashtag': f'#{topic_clean}tips', 'usage_count': 800, 'engagement': 'medium'},
        ]
        
        return {
            'real_hashtags': fallback[:3],
            'ai_hashtags': fallback[3:],
            'combined': [h['hashtag'] for h in fallback]
        }
