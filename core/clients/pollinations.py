import requests
from urllib.parse import quote
from core.utils.retry import retry_with_backoff
from core.exceptions import AIServiceUnavailable

class PollinationsClient:
    BASE_URL = "https://image.pollinations.ai/prompt"
    
    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def generate_thumbnail(self, prompt: str, width: int = 1280, height: int = 720) -> str:
        """Generate thumbnail using Pollinations AI (free, no API key needed). Returns image URL."""
        try:
            enhanced_prompt = f"Professional YouTube thumbnail: {prompt}. High quality, eye-catching, vibrant colors."
            encoded_prompt = quote(enhanced_prompt)
            
            # Pollinations returns the image directly at this URL
            image_url = f"{self.BASE_URL}/{encoded_prompt}?width={width}&height={height}&nologo=true"
            
            # Verify the URL works
            response = requests.head(image_url, timeout=30)
            if response.status_code == 200:
                return image_url
            
            raise AIServiceUnavailable('Pollinations failed to generate image')
            
        except requests.RequestException as e:
            raise AIServiceUnavailable(f'Pollinations error: {str(e)}')
    
    def is_available(self) -> bool:
        """Pollinations is always available (free service)"""
        return True

pollinations_client = PollinationsClient()
