import base64
import requests
from io import BytesIO
from django.conf import settings
from imagekitio import ImageKit
from core.utils.retry import retry_with_backoff
from core.exceptions import InsightStreamException

class ImageKitClient:
    def __init__(self):
        self._client = None
    
    def _get_client(self) -> ImageKit:
        if not self._client:
            if not all([settings.IMAGEKIT_PUBLIC_KEY, settings.IMAGEKIT_PRIVATE_KEY, settings.IMAGEKIT_URL_ENDPOINT]):
                raise InsightStreamException('ImageKit not configured', 'CONFIG_ERROR')
            
            self._client = ImageKit(
                public_key=settings.IMAGEKIT_PUBLIC_KEY,
                private_key=settings.IMAGEKIT_PRIVATE_KEY,
                url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
            )
        return self._client
    
    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def upload_from_url(self, image_url: str, file_name: str = 'thumbnail') -> str:
        """Download image from URL and upload to ImageKit. Returns CDN URL."""
        try:
            # Download image
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            # Convert to base64
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            
            # Upload to ImageKit
            client = self._get_client()
            result = client.upload_file(
                file=image_base64,
                file_name=f"{file_name}.png",
                options={
                    "folder": "/thumbnails/",
                    "use_unique_file_name": True,
                }
            )
            
            if result.url:
                return result.url
            raise InsightStreamException('ImageKit upload failed', 'UPLOAD_ERROR')
            
        except requests.RequestException as e:
            raise InsightStreamException(f'Failed to download image: {str(e)}', 'DOWNLOAD_ERROR')
        except Exception as e:
            raise InsightStreamException(f'ImageKit error: {str(e)}', 'IMAGEKIT_ERROR')
    
    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def upload_from_bytes(self, image_bytes: bytes, file_name: str = 'thumbnail') -> str:
        """Upload image bytes to ImageKit. Returns CDN URL."""
        try:
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            client = self._get_client()
            result = client.upload_file(
                file=image_base64,
                file_name=f"{file_name}.png",
                options={
                    "folder": "/thumbnails/",
                    "use_unique_file_name": True,
                }
            )
            
            if result.url:
                return result.url
            raise InsightStreamException('ImageKit upload failed', 'UPLOAD_ERROR')
            
        except Exception as e:
            raise InsightStreamException(f'ImageKit error: {str(e)}', 'IMAGEKIT_ERROR')
    
    def is_available(self) -> bool:
        return all([settings.IMAGEKIT_PUBLIC_KEY, settings.IMAGEKIT_PRIVATE_KEY, settings.IMAGEKIT_URL_ENDPOINT])

imagekit_client = ImageKitClient()
