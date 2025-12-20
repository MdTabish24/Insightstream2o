#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insightstream.settings')
django.setup()

from apps.hashtags.services import HashtagService

print("=" * 50)
print("Testing Hashtag Service")
print("=" * 50)

service = HashtagService()

print("\nGenerating hashtags for 'fighting'...")
try:
    result = service.generate_hashtags("fighting")
    
    print(f"\nReal Hashtags ({len(result['real_hashtags'])}):")
    for item in result['real_hashtags'][:5]:
        if isinstance(item, dict):
            print(f"  {item['hashtag']} - {item['engagement']}")
        else:
            print(f"  {item}")
    
    print(f"\nAI Hashtags ({len(result['ai_hashtags'])}):")
    for item in result['ai_hashtags'][:5]:
        if isinstance(item, dict):
            print(f"  {item['hashtag']} - {item['engagement']}")
        else:
            print(f"  {item}")
    
    print(f"\nCombined ({len(result['combined'])}):")
    for tag in result['combined'][:10]:
        print(f"  {tag}")
    
    print("\nSuccess!")
    
except Exception as e:
    print(f"\nError: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
