import hashlib

def md5_url_encode(url: str, length: int = 10) -> str:
    """
    Gera um hash MD5 da URL e retorna os primeiros 'length' caracteres.
    
    Args:
        url (str): URL a ser codificada.
        length (int, opcional): Tamanho do hash retornado. Padrão é 10.
    
    Returns:
        str: Hash MD5 truncado.
    
    Raises:
        ValueError: Se a URL for vazia.
    """

    if not url:
        raise ValueError("A URL não pode ser vazia.")

    return hashlib.md5(url.encode('utf-8')).hexdigest()[:length]
