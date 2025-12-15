import time
import requests
from urllib.parse import quote
from core.utils.retry import retry_with_backoff
from core.exceptions import AIServiceUnavailable

class PollinationsClient:
    BASE_URL = "https://image.pollinations.ai/prompt"
    
    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def generate_thumbnail(self, prompt: str, width: int = 1280, height: int = 720) -> str:
        """Generate thumbnail using Pollinations AI (free, no API key needed). Returns image URL."""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"[Pollinations] Starting generation for prompt: {prompt[:50]}...")
            enhanced_prompt = f"Professional YouTube thumbnail: {prompt.strip()}. High quality, eye-catching, vibrant colors."
            encoded_prompt = quote(enhanced_prompt, safe='')
            logger.info(f"[Pollinations] Encoded prompt length: {len(encoded_prompt)}")
            
            seed = int(time.time() * 1000)
            image_url = f"{self.BASE_URL}/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={seed}&model=flux"
            logger.info(f"[Pollinations] Generated URL (first 150 chars): {image_url[:150]}...")
            logger.info(f"[Pollinations] Full URL length: {len(image_url)}, seed: {seed}")
            
            logger.info(f"[Pollinations] Fetching image to verify...")
            response = requests.get(image_url, timeout=60, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
            logger.info(f"[Pollinations] Response: status={response.status_code}, content-type={response.headers.get('content-type')}, size={len(response.content)}")
            
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image/'):
                logger.info(f"[Pollinations] Success! Image generated and verified")
                return image_url
            
            logger.error(f"[Pollinations] Failed: status={response.status_code}, content-type={response.headers.get('content-type')}")
            raise AIServiceUnavailable(f'Pollinations failed: status={response.status_code}, content-type={response.headers.get("content-type")}')
            
        except requests.RequestException as e:
            logger.error(f"[Pollinations] Request error: {str(e)}", exc_info=True)
            raise AIServiceUnavailable(f'Pollinations error: {str(e)}')
    
    def is_available(self) -> bool:
        """Pollinations is always available (free service)"""
        import logging
        logger = logging.getLogger(__name__)
        logger.info("[Pollinations] Checking availability: Always available")
        return True

pollinations_client = PollinationsClient()
