import logging
from datetime import datetime
from .models import Thumbnail
from core.clients.replicate import replicate_client
from core.clients.pollinations import pollinations_client
from core.clients.imagekit_client import imagekit_client
from core.exceptions import AIServiceUnavailable, InsightStreamException

logger = logging.getLogger(__name__)

class ThumbnailService:
    """
    Service for generating AI thumbnails with fallback support.
    Primary: Replicate FLUX
    Fallback: Pollinations AI
    CDN: ImageKit
    """
    
    def generate_thumbnail(self, prompt: str, user, ref_image: str = None) -> dict:
        """
        Generate thumbnail using AI with automatic fallback.
        
        Requirements:
        - 2.1: Use FLUX AI model via Replicate
        - 2.2: Fallback to Pollinations if Replicate fails
        - 2.3: Upload to ImageKit CDN and store in database
        - 2.6: 16:9 aspect ratio, PNG format
        """
        generated_url = None
        cdn_url = None
        provider_used = None
        
        try:
            # Try primary provider (Replicate FLUX)
            if replicate_client.is_available():
                try:
                    logger.info(f"Attempting thumbnail generation with Replicate for user {user.email}")
                    generated_url = replicate_client.generate_thumbnail(prompt, aspect_ratio="16:9")
                    provider_used = 'replicate'
                    logger.info(f"Successfully generated thumbnail with Replicate: {generated_url}")
                except AIServiceUnavailable as e:
                    logger.warning(f"Replicate failed: {str(e)}. Falling back to Pollinations.")
                    generated_url = None
            
            # Fallback to Pollinations if Replicate failed or unavailable
            if not generated_url:
                logger.info(f"Using Pollinations fallback for user {user.email}")
                generated_url = pollinations_client.generate_thumbnail(prompt, width=1280, height=720)
                provider_used = 'pollinations'
                logger.info(f"Successfully generated thumbnail with Pollinations: {generated_url}")
            
            # Upload to ImageKit CDN if configured
            if imagekit_client.is_available():
                try:
                    logger.info(f"Uploading thumbnail to ImageKit CDN")
                    cdn_url = imagekit_client.upload_from_url(
                        generated_url, 
                        file_name=f"thumbnail_{user.id}_{datetime.now().timestamp()}"
                    )
                    logger.info(f"Successfully uploaded to ImageKit: {cdn_url}")
                except InsightStreamException as e:
                    logger.warning(f"ImageKit upload failed: {str(e)}. Using direct URL.")
                    cdn_url = generated_url
            else:
                logger.info("ImageKit not configured, using direct URL")
                cdn_url = generated_url
            
            # Save to database
            thumbnail = Thumbnail.objects.create(
                user=user,
                user_input=prompt,
                thumbnail_url=cdn_url,
                ref_image=ref_image
            )
            
            logger.info(f"Thumbnail saved to database with ID {thumbnail.id}")
            
            return {
                'id': thumbnail.id,
                'thumbnail_url': thumbnail.thumbnail_url,
                'prompt': thumbnail.user_input,
                'ref_image': thumbnail.ref_image,
                'provider': provider_used,
                'created_at': thumbnail.created_at.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Thumbnail generation failed completely: {str(e)}")
            raise AIServiceUnavailable(f'Failed to generate thumbnail: {str(e)}')
    
    def get_user_thumbnails(self, user) -> list:
        """Get all thumbnails for a user, ordered by creation date (newest first)"""
        thumbnails = Thumbnail.objects.filter(user=user)
        return [
            {
                'id': t.id,
                'thumbnail_url': t.thumbnail_url,
                'prompt': t.user_input,
                'ref_image': t.ref_image,
                'created_at': t.created_at.isoformat()
            }
            for t in thumbnails
        ]

thumbnail_service = ThumbnailService()
