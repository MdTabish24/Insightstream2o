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
        try:
            client = self._get_client()
            
            enhanced_prompt = f"Professional YouTube thumbnail: {prompt}. High quality, eye-catching, vibrant colors, clear text if any."
            
            output = client.run(
                self.FLUX_MODEL,
                input={
                    "prompt": enhanced_prompt,
                    "aspect_ratio": aspect_ratio,
                    "output_format": "png",
                    "num_outputs": 1
                }
            )
            
            # Output is a list of URLs
            if output and len(output) > 0:
                return str(output[0])
            raise AIServiceUnavailable('No image generated')
            
        except Exception as e:
            if 'rate' in str(e).lower() or 'limit' in str(e).lower():
                api_key_manager.rotate_key('replicate')
            raise AIServiceUnavailable(f'Replicate error: {str(e)}')
    
    def is_available(self) -> bool:
        return bool(api_key_manager.get_active_key('replicate'))

replicate_client = ReplicateClient()
