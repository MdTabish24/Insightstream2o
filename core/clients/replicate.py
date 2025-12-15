import replicate
from django.conf import settings
from core.utils.api_key_manager import api_key_manager
from core.utils.retry import retry_with_backoff
from core.exceptions import AIServiceUnavailable

class ReplicateClient:
    FLUX_MODEL = "black-forest-labs/flux-schnell"
    
    def __init__(self):
        self.client = None
    
    def _get_client(self):
        api_key = api_key_manager.get_active_key('replicate')
        if not api_key:
            raise AIServiceUnavailable('No Replicate API key available')
        return replicate.Client(api_token=api_key)
    
    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def generate_thumbnail(self, prompt: str, aspect_ratio: str = "16:9") -> str:
        """Generate thumbnail using FLUX model. Returns image URL."""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"[Replicate] Starting generation for prompt: {prompt[:50]}...")
            client = self._get_client()
            logger.info(f"[Replicate] Client initialized, using model: {self.FLUX_MODEL}")
            
            enhanced_prompt = f"Professional YouTube thumbnail: {prompt}. High quality, eye-catching, vibrant colors, clear text if any."
            logger.info(f"[Replicate] Enhanced prompt length: {len(enhanced_prompt)}")
            
            logger.info(f"[Replicate] Calling API with aspect_ratio={aspect_ratio}...")
            output = client.run(
                self.FLUX_MODEL,
                input={
                    "prompt": enhanced_prompt,
                    "aspect_ratio": aspect_ratio,
                    "output_format": "png",
                    "num_outputs": 1
                }
            )
            logger.info(f"[Replicate] API response type: {type(output)}, length: {len(output) if output else 0}")
            
            if output and len(output) > 0:
                url = str(output[0])
                logger.info(f"[Replicate] Success! Generated URL: {url}")
                return url
            
            logger.error(f"[Replicate] No image in output: {output}")
            raise AIServiceUnavailable('No image generated')
            
        except Exception as e:
            logger.error(f"[Replicate] Error: {str(e)}", exc_info=True)
            if 'rate' in str(e).lower() or 'limit' in str(e).lower():
                logger.warning(f"[Replicate] Rate limit detected, rotating key...")
                api_key_manager.rotate_key('replicate')
            raise AIServiceUnavailable(f'Replicate error: {str(e)}')
    
    def is_available(self) -> bool:
        import logging
        logger = logging.getLogger(__name__)
        available = bool(api_key_manager.get_active_key('replicate'))
        logger.info(f"[Replicate] Checking availability: {available}")
        return available

replicate_client = ReplicateClient()
