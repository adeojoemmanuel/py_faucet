from django.core.cache import cache
from django.conf import settings

def check_rate_limit(ip, wallet):
    ip_key = f'rate_limit:{ip}'
    wallet_key = f'rate_limit:{wallet}'
    
    if cache.get(ip_key) or cache.get(wallet_key):
        return False
    
    timeout = getattr(settings, 'RATE_LIMIT_TIMEOUT', 60)
    cache.set(ip_key, True, timeout)
    cache.set(wallet_key, True, timeout)
    return True