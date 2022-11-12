from settings import env

REDIS_BASE_URL = env("REDIS_BASE_URL", default="redis://redis:6379")

CACHES = {
    'redis_cache': {
        'BACKEND': "django_redis.cache.RedisCache",
        'LOCATION': f'{REDIS_BASE_URL}/1',
        'TIMEOUT': 864000,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '',
    }
}
