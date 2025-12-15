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
            logger.info(f"[ThumbnailService] ===== STARTING GENERATION =====")
            logger.info(f"[ThumbnailService] User: {user.email}, Prompt: {prompt[:100]}...")
            
            # Try primary provider (Replicate FLUX)
            if replicate_client.is_available():
                try:
                    logger.info(f"[ThumbnailService] Attempting Replicate FLUX...")
                    generated_url = replicate_client.generate_thumbnail(prompt, aspect_ratio="16:9")
                    provider_used = 'replicate'
                    logger.info(f"[ThumbnailService] ✓ Replicate SUCCESS: {generated_url}")
                except AIServiceUnavailable as e:
                    logger.warning(f"[ThumbnailService] ✗ Replicate FAILED: {str(e)}")
                    logger.info(f"[ThumbnailService] Falling back to Pollinations...")
                    generated_url = None
            else:
                logger.info(f"[ThumbnailService] Replicate not available, using Pollinations")
            
            # Fallback to Pollinations if Replicate failed or unavailable
            if not generated_url:
                logger.info(f"[ThumbnailService] Attempting Pollinations...")
                generated_url = pollinations_client.generate_thumbnail(prompt, width=1280, height=720)
                provider_used = 'pollinations'
                logger.info(f"[ThumbnailService] ✓ Pollinations SUCCESS: {generated_url[:100]}...")
            
            # Upload to ImageKit CDN if configured
            logger.info(f"[ThumbnailService] ----- CDN UPLOAD PHASE -----")
            if imagekit_client.is_available():
                try:
                    logger.info(f"[ThumbnailService] ImageKit available, starting upload...")
                    logger.info(f"[ThumbnailService] Source URL: {generated_url[:100]}...")
                    cdn_url = imagekit_client.upload_from_url(
                        generated_url, 
                        file_name=f"thumbnail_{user.id}_{int(datetime.now().timestamp())}"
                    )
                    logger.info(f"[ThumbnailService] ✓ ImageKit SUCCESS: {cdn_url}")
                except InsightStreamException as e:
                    logger.error(f"[ThumbnailService] ✗ ImageKit FAILED: {str(e)}")
                    logger.info(f"[ThumbnailService] Using direct URL as fallback")
                    cdn_url = generated_url
                except Exception as e:
                    logger.error(f"[ThumbnailService] ✗ ImageKit UNEXPECTED ERROR: {str(e)}", exc_info=True)
                    logger.info(f"[ThumbnailService] Using direct URL as fallback")
                    cdn_url = generated_url
            else:
                logger.info(f"[ThumbnailService] ImageKit not configured, using direct URL")
                cdn_url = generated_url
            
            # Validate URL before saving
            logger.info(f"[ThumbnailService] ----- VALIDATION & SAVE PHASE -----")
            logger.info(f"[ThumbnailService] Final URL: {cdn_url}")
            if not cdn_url or not cdn_url.startswith('http'):
                logger.error(f"[ThumbnailService] ✗ INVALID URL: {cdn_url}")
                raise AIServiceUnavailable('Failed to generate valid thumbnail URL')
            logger.info(f"[ThumbnailService] ✓ URL validation passed")
            
            # Save to database
            logger.info(f"[ThumbnailService] Saving to database...")
            thumbnail = Thumbnail.objects.create(
                user=user,
                user_input=prompt,
                thumbnail_url=cdn_url,
                ref_image=ref_image
            )
            logger.info(f"[ThumbnailService] ✓ Saved to DB with ID: {thumbnail.id}")
            
            result = {
                'id': thumbnail.id,
                'thumbnail_url': thumbnail.thumbnail_url,
                'prompt': thumbnail.user_input,
                'ref_image': thumbnail.ref_image,
                'provider': provider_used,
                'created_at': thumbnail.created_at.isoformat()
            }
            logger.info(f"[ThumbnailService] ===== GENERATION COMPLETE =====")
            logger.info(f"[ThumbnailService] Result: ID={result['id']}, Provider={provider_used}")
            return result
            
        except Exception as e:
            logger.error(f"[ThumbnailService] ===== GENERATION FAILED =====")
            logger.error(f"[ThumbnailService] Error: {str(e)}", exc_info=True)
            raise AIServiceUnavailable(f'Failed to generate thumbnail: {str(e)}')
    
    def get_user_thumbnails(self, user) -> list:
        """Get all thumbnails for a user, ordered by creation date (newest first)"""
        logger.info(f"[ThumbnailService] Getting thumbnails for user: {user.email}")
        thumbnails = Thumbnail.objects.filter(user=user)
        logger.info(f"[ThumbnailService] Found {thumbnails.count()} thumbnails")
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
