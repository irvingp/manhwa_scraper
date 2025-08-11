from urllib.parse import urlparse
import re

def extract_manwha_name(url):
    parts = urlparse(url).path.split('/')
    return parts[3] if len(parts) > 3 else "manwha"

def sanitize_filename(name):
    # Reemplaza caracteres no válidos por guiones bajos
    return re.sub(r'[\\/*?:"<>|]', "_", name)