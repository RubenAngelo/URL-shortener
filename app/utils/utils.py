import hashlib

def md5_url_encode(url: str, length: int = 10) -> str:
    return hashlib.md5(url.encode('utf-8')).hexdigest()[:length]
