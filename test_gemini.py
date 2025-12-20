#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insightstream.settings')
django.setup()

from django.conf import settings
from core.clients.gemini import gemini_client

print("=" * 50)
print("Testing Gemini API Configuration")
print("=" * 50)

# Check API keys
print(f"\nGemini API Keys configured: {len(settings.GEMINI_API_KEYS)}")
for i, key in enumerate(settings.GEMINI_API_KEYS, 1):
    masked = key[:10] + "..." + key[-4:] if len(key) > 14 else "***"
    print(f"  Key {i}: {masked}")

# Test API call
print("\nTesting hashtag generation...")
try:
    result = gemini_client.generate_hashtags("fighting")
    print(f"Success! Generated {len(result)} hashtags:")
    for tag in result:
        print(f"  - {tag}")
except Exception as e:
    print(f"Error: {str(e)}")
    print(f"Error type: {type(e).__name__}")

print("\n" + "=" * 50)
