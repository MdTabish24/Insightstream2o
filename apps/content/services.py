import logging
from .models import AIContent
from core.clients.gemini import gemini_client
from core.exceptions import AIServiceUnavailable

logger = logging.getLogger(__name__)

class ContentService:
    """
    Service for generating AI video content concepts.
    
    Requirements:
    - 3.1: Generate 3 unique video concepts
    - 3.2: Include SEO scores (0-100)
    - 3.3: Include hooks, main content, CTAs
    - 3.4: Fallback on AI failure
    - 3.5: Store in database with user association
    """
    
    def generate_content(self, topic: str, user) -> dict:
        """
        Generate 3 unique video concepts with SEO optimization.
        
        Returns:
        {
            'id': int,
            'content': {
                'concepts': [
                    {
                        'title': str,
                        'seo_score': int (0-100),
                        'description': {
                            'hook': str,
                            'main_content': str,
                            'cta': str
                        },
                        'tags': list[str]
                    }
                ]
            },
            'created_at': str
        }
        """
        try:
            logger.info(f"Generating content for topic '{topic}' for user {user.email}")
            
            # Generate content using Gemini AI
            content_data = gemini_client.generate_video_concepts(topic)
            
            # Validate structure
            if not self._validate_content_structure(content_data):
                logger.warning("AI generated invalid structure, using fallback")
                content_data = self._get_fallback_content(topic)
            
            # Ensure exactly 3 concepts
            if len(content_data.get('concepts', [])) != 3:
                logger.warning(f"AI generated {len(content_data.get('concepts', []))} concepts, expected 3")
                content_data = self._get_fallback_content(topic)
            
            logger.info(f"Successfully generated {len(content_data['concepts'])} concepts")
            
        except AIServiceUnavailable as e:
            logger.error(f"AI service unavailable: {str(e)}, using fallback")
            content_data = self._get_fallback_content(topic)
        except Exception as e:
            logger.error(f"Unexpected error during content generation: {str(e)}, using fallback")
            content_data = self._get_fallback_content(topic)
        
        # Save to database
        ai_content = AIContent.objects.create(
            user=user,
            user_input=topic,
            content=content_data
        )
        
        logger.info(f"Content saved to database with ID {ai_content.id}")
        
        return {
            'id': ai_content.id,
            'topic': topic,
            'content': content_data,
            'created_at': ai_content.created_at.isoformat()
        }
    
    def get_user_content(self, user) -> list:
        """Get all content for a user, ordered by creation date (newest first)"""
        contents = AIContent.objects.filter(user=user)
        return [
            {
                'id': c.id,
                'topic': c.user_input,
                'content': c.content,
                'created_at': c.created_at.isoformat()
            }
            for c in contents
        ]
    
    def _validate_content_structure(self, content_data: dict) -> bool:
        """Validate that content has the required structure"""
        if not isinstance(content_data, dict):
            return False
        
        if 'concepts' not in content_data:
            return False
        
        concepts = content_data['concepts']
        if not isinstance(concepts, list) or len(concepts) == 0:
            return False
        
        # Validate each concept
        for concept in concepts:
            if not isinstance(concept, dict):
                return False
            
            # Check required fields
            if 'title' not in concept or 'seo_score' not in concept:
                return False
            
            if 'description' not in concept or not isinstance(concept['description'], dict):
                return False
            
            desc = concept['description']
            if 'hook' not in desc or 'main_content' not in desc or 'cta' not in desc:
                return False
            
            if 'tags' not in concept or not isinstance(concept['tags'], list):
                return False
            
            # Validate SEO score range
            if not isinstance(concept['seo_score'], (int, float)) or not (0 <= concept['seo_score'] <= 100):
                return False
        
        return True
    
    def _get_fallback_content(self, topic: str) -> dict:
        """Generate fallback content when AI fails"""
        return {
            'concepts': [
                {
                    'title': f'{topic} - Complete Guide for Beginners',
                    'seo_score': 72,
                    'description': {
                        'hook': f'Want to master {topic}? This complete guide has everything you need!',
                        'main_content': f'In this comprehensive video, we cover all the essentials of {topic}. From basic concepts to advanced techniques, you\'ll learn step-by-step how to get started and succeed.',
                        'cta': 'Subscribe for more tutorials and hit the bell icon to never miss an update!'
                    },
                    'tags': [topic, 'tutorial', 'guide', 'beginners', 'how to']
                },
                {
                    'title': f'Top 10 {topic} Tips and Tricks You Need to Know',
                    'seo_score': 68,
                    'description': {
                        'hook': f'Discover the secret tips that professionals use for {topic}!',
                        'main_content': f'Learn the top 10 tips and tricks that will take your {topic} skills to the next level. These proven strategies will save you time and help you achieve better results.',
                        'cta': 'Like this video if you found it helpful and share it with others!'
                    },
                    'tags': [topic, 'tips', 'tricks', 'hacks', 'pro tips']
                },
                {
                    'title': f'{topic} Explained: Everything You Need to Know in 2024',
                    'seo_score': 76,
                    'description': {
                        'hook': f'Confused about {topic}? Let me break it down for you in simple terms!',
                        'main_content': f'This video explains everything about {topic} in an easy-to-understand way. Perfect for anyone looking to learn quickly and effectively in 2024.',
                        'cta': 'Don\'t forget to subscribe and turn on notifications for more content like this!'
                    },
                    'tags': [topic, 'explained', '2024', 'education', 'learning']
                }
            ]
        }

content_service = ContentService()
