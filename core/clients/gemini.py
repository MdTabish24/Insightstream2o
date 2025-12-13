import json
import google.generativeai as genai
from django.conf import settings
from core.utils.api_key_manager import api_key_manager
from core.utils.retry import retry_with_backoff
from core.exceptions import AIServiceUnavailable, RateLimitExceeded

class GeminiClient:
    def __init__(self):
        self.model_name = 'gemini-2.0-flash'
    
    def _get_model(self):
        api_key = api_key_manager.get_active_key('gemini')
        if not api_key:
            raise AIServiceUnavailable('No Gemini API key available')
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(self.model_name)
    
    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def generate_content(self, prompt: str) -> str:
        try:
            model = self._get_model()
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if 'quota' in str(e).lower() or 'rate' in str(e).lower():
                api_key_manager.rotate_key('gemini')
                if api_key_manager.is_exhausted('gemini'):
                    raise RateLimitExceeded('All Gemini API keys exhausted')
                return self.generate_content(prompt)
            raise AIServiceUnavailable(f'Gemini error: {str(e)}')
    
    def generate_video_concepts(self, topic: str) -> dict:
        prompt = f"""Generate 3 unique YouTube video concepts for the topic: "{topic}"
        
Return ONLY valid JSON in this exact format:
{{
    "concepts": [
        {{
            "title": "Video title here",
            "seo_score": 85,
            "description": {{
                "hook": "Opening hook to grab attention",
                "main_content": "Main video description",
                "cta": "Call to action"
            }},
            "tags": ["tag1", "tag2", "tag3"]
        }}
    ]
}}

Make each concept unique and SEO-optimized. SEO score should be 0-100."""
        
        response = self.generate_content(prompt)
        try:
            # Clean response and parse JSON
            text = response.strip()
            if text.startswith('```'):
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
            return json.loads(text.strip())
        except json.JSONDecodeError:
            return self._fallback_content(topic)
    
    def generate_keywords(self, topic: str) -> dict:
        prompt = f"""Research keywords for YouTube topic: "{topic}"

Return ONLY valid JSON:
{{
    "primary_keywords": [{{"keyword": "...", "search_volume": 10000, "competition": "medium", "relevance": 0.9}}],
    "long_tail_keywords": [{{"keyword": "...", "search_volume": 5000, "competition": "low", "relevance": 0.85}}],
    "trending_keywords": [{{"keyword": "...", "search_volume": 8000, "competition": "high", "relevance": 0.8}}],
    "related_topics": [{{"topic": "...", "search_volume": 6000, "competition": "medium", "relevance": 0.75}}]
}}"""
        
        response = self.generate_content(prompt)
        try:
            text = response.strip()
            if text.startswith('```'):
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
            return json.loads(text.strip())
        except json.JSONDecodeError:
            return self._fallback_keywords(topic)
    
    def generate_hashtags(self, topic: str) -> list:
        prompt = f"""Generate 10 trending YouTube hashtags for: "{topic}"
Return ONLY a JSON array of hashtags like: ["#hashtag1", "#hashtag2"]"""
        
        response = self.generate_content(prompt)
        try:
            text = response.strip()
            if text.startswith('```'):
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
            return json.loads(text.strip())
        except json.JSONDecodeError:
            return [f'#{topic}', '#youtube', '#viral', '#trending']
    
    def analyze_thumbnail(self, image_url: str) -> list:
        prompt = f"""Analyze this YouTube thumbnail and generate descriptive tags.
Image URL: {image_url}
Return ONLY a JSON array of tags like: ["tag1", "tag2", "tag3"]"""
        
        response = self.generate_content(prompt)
        try:
            text = response.strip()
            if text.startswith('```'):
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
            return json.loads(text.strip())
        except json.JSONDecodeError:
            return ['thumbnail', 'youtube', 'video']
    
    def generate_growth_suggestions(self, channel_data: dict) -> list:
        prompt = f"""Based on this YouTube channel data, provide growth suggestions:
{json.dumps(channel_data)}
Return ONLY a JSON array of suggestions like: ["suggestion1", "suggestion2"]"""
        
        response = self.generate_content(prompt)
        try:
            text = response.strip()
            if text.startswith('```'):
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
            return json.loads(text.strip())
        except json.JSONDecodeError:
            return ['Post more consistently', 'Engage with your audience', 'Optimize thumbnails']
    
    def _fallback_content(self, topic: str) -> dict:
        return {
            'concepts': [
                {
                    'title': f'{topic} - Complete Guide',
                    'seo_score': 70,
                    'description': {'hook': f'Learn about {topic}', 'main_content': f'Everything about {topic}', 'cta': 'Subscribe!'},
                    'tags': [topic, 'tutorial', 'guide']
                },
                {
                    'title': f'{topic} Tips and Tricks',
                    'seo_score': 65,
                    'description': {'hook': f'Master {topic}', 'main_content': f'Pro tips for {topic}', 'cta': 'Like and subscribe!'},
                    'tags': [topic, 'tips', 'tricks']
                },
                {
                    'title': f'{topic} for Beginners',
                    'seo_score': 75,
                    'description': {'hook': f'Start with {topic}', 'main_content': f'Beginner guide to {topic}', 'cta': 'Join us!'},
                    'tags': [topic, 'beginners', 'tutorial']
                }
            ]
        }
    
    def _fallback_keywords(self, topic: str) -> dict:
        return {
            'primary_keywords': [{'keyword': topic, 'search_volume': 10000, 'competition': 'medium', 'relevance': 0.9}],
            'long_tail_keywords': [{'keyword': f'how to {topic}', 'search_volume': 5000, 'competition': 'low', 'relevance': 0.85}],
            'trending_keywords': [{'keyword': f'{topic} 2024', 'search_volume': 8000, 'competition': 'high', 'relevance': 0.8}],
            'related_topics': [{'topic': f'{topic} tutorial', 'search_volume': 6000, 'competition': 'medium', 'relevance': 0.75}]
        }

gemini_client = GeminiClient()
