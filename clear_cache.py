#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insightstream.settings')
django.setup()

from django.core.cache import cache

# Clear all rate limit cache
cache.clear()
print("Cache cleared! API keys reset.")
