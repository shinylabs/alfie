from django.core.cache import cache

def cached_queries():
    return {'cache', cache.get('key')