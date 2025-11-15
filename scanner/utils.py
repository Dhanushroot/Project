from urllib.parse import urlparse
import requests

def sanitize_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ('http','https') and parsed.netloc != ''
    except Exception:
        return False

def timed_request(url, timeout=5):
    return requests.get(url, timeout=timeout)
