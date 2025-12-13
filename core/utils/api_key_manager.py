from django.conf import settings
from django.core.cache import cache
import time

class APIKeyManager:
    def __init__(self):
        self.keys = {
            'gemini': settings.GEMINI_API_KEYS,
            'replicate': [settings.REPLICATE_API_TOKEN] if settings.REPLICATE_API_TOKEN else [],
            'youtube': [settings.YOUTUBE_API_KEY] if settings.YOUTUBE_API_KEY else [],
        }
        self.current_index = {}
    
    def get_active_key(self, service: str) -> str:
        keys = self.keys.get(service, [])
        if not keys:
            return ''
        idx = self.current_index.get(service, 0)
        return keys[idx % len(keys)]
    
    def rotate_key(self, service: str) -> str:
        keys = self.keys.get(service, [])
        if not keys:
            return ''
        current = self.current_index.get(service, 0)
        self.current_index[service] = (current + 1) % len(keys)
        cache.set(f'rate_limited_{service}_{current}', True, timeout=60)
        return self.get_active_key(service)
    
    def mark_rate_limited(self, service: str, key: str) -> None:
        cache.set(f'rate_limited_{service}_{key}', True, timeout=60)
    
    def is_exhausted(self, service: str) -> bool:
        keys = self.keys.get(service, [])
        return all(cache.get(f'rate_limited_{service}_{i}') for i in range(len(keys)))

api_key_manager = APIKeyManager()
