import base64
import requests
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
    
    @retry_with_backoff(max_retries=2, base_delay=1.0)
    def upload_from_url(self, image_url: str, file_name: str = 'thumbnail') -> str:
        """Download image from URL and upload to ImageKit. Returns CDN URL."""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"[ImageKit] Starting download from URL: {image_url[:100]}...")
            response = requests.get(
                image_url, 
                timeout=60,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response.raise_for_status()
            logger.info(f"[ImageKit] Downloaded {len(response.content)} bytes, content-type: {response.headers.get('content-type')}")
            
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                logger.error(f"[ImageKit] Invalid content type: {content_type}")
                raise InsightStreamException(f'Invalid content type: {content_type}', 'INVALID_IMAGE')
            
            logger.info(f"[ImageKit] Converting to base64 with data URI...")
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            data_uri = f"data:{content_type};base64,{image_base64}"
            logger.info(f"[ImageKit] Data URI length: {len(data_uri)}")
            
            logger.info(f"[ImageKit] Uploading to ImageKit with filename: {file_name}.png")
            client = self._get_client()
            from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
            options = UploadFileRequestOptions(
                folder="/thumbnails/",
                use_unique_file_name=True,
            )
            result = client.upload_file(
                file=data_uri,
                file_name=f"{file_name}.png",
                options=options
            )
            logger.info(f"[ImageKit] Upload result type: {type(result)}, has url attr: {hasattr(result, 'url')}")
            
            if hasattr(result, 'url') and result.url:
                logger.info(f"[ImageKit] Success! URL from result.url: {result.url}")
                return result.url
            elif isinstance(result, dict) and 'url' in result:
                logger.info(f"[ImageKit] Success! URL from dict: {result['url']}")
                return result['url']
            elif hasattr(result, 'response_metadata'):
                logger.info(f"[ImageKit] Checking response_metadata...")
                if hasattr(result.response_metadata, 'url'):
                    logger.info(f"[ImageKit] Success! URL from metadata.url: {result.response_metadata.url}")
                    return result.response_metadata.url
                if hasattr(result.response_metadata, 'raw') and isinstance(result.response_metadata.raw, dict):
                    url = result.response_metadata.raw.get('url')
                    if url:
                        logger.info(f"[ImageKit] Success! URL from metadata.raw: {url}")
                        return url
            
            logger.error(f"[ImageKit] No URL found in result. Type: {type(result)}, Dir: {dir(result)[:5]}")
            raise InsightStreamException(f'ImageKit upload failed: No URL in response. Result type: {type(result)}', 'UPLOAD_ERROR')
            
        except requests.RequestException as e:
            logger.error(f"[ImageKit] Download failed: {str(e)}")
            raise InsightStreamException(f'Failed to download image: {str(e)}', 'DOWNLOAD_ERROR')
        except InsightStreamException:
            raise
        except Exception as e:
            logger.error(f"[ImageKit] Unexpected error: {str(e)}", exc_info=True)
            raise InsightStreamException(f'ImageKit error: {str(e)}', 'IMAGEKIT_ERROR')
    
    @retry_with_backoff(max_retries=2, base_delay=1.0)
    def upload_from_bytes(self, image_bytes: bytes, file_name: str = 'thumbnail') -> str:
        """Upload image bytes to ImageKit. Returns CDN URL."""
        try:
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            data_uri = f"data:image/png;base64,{image_base64}"
            
            client = self._get_client()
            from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
            options = UploadFileRequestOptions(
                folder="/thumbnails/",
                use_unique_file_name=True,
            )
            result = client.upload_file(
                file=data_uri,
                file_name=f"{file_name}.png",
                options=options
            )
            
            if hasattr(result, 'url') and result.url:
                return result.url
            elif isinstance(result, dict) and 'url' in result:
                return result['url']
            elif hasattr(result, 'response_metadata'):
                if hasattr(result.response_metadata, 'url'):
                    return result.response_metadata.url
                if hasattr(result.response_metadata, 'raw') and isinstance(result.response_metadata.raw, dict):
                    url = result.response_metadata.raw.get('url')
                    if url:
                        return url
            raise InsightStreamException(f'ImageKit upload failed: No URL. Result type: {type(result)}', 'UPLOAD_ERROR')
            
        except Exception as e:
            raise InsightStreamException(f'ImageKit error: {str(e)}', 'IMAGEKIT_ERROR')
    
    def is_available(self) -> bool:
        return all([settings.IMAGEKIT_PUBLIC_KEY, settings.IMAGEKIT_PRIVATE_KEY, settings.IMAGEKIT_URL_ENDPOINT])

imagekit_client = ImageKitClient()
