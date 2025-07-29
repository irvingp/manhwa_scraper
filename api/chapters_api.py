import requests
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

class ChaptersAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def _build_url(self, page):
        url_parts = list(urlparse(self.base_url))
        query = parse_qs(url_parts[4])
        query['page'] = [str(page)]
        url_parts[4] = urlencode(query, doseq=True)
        return urlunparse(url_parts)

    def get_chapters(self):
        """Obtiene todos los capítulos manejando paginación."""
        all_chapters = []

        first_response = requests.get(self._build_url(1))
        first_response.raise_for_status()
        first_data = first_response.json()

        last_page = first_data.get("meta", {}).get("last_page", 1)
        all_chapters.extend(first_data["data"])
        print(f"📄 Página 1/{last_page} descargada ({len(first_data['data'])} capítulos)")

        for page in range(2, last_page + 1):
            url = self._build_url(page)
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            all_chapters.extend(data["data"])
            print(f"📄 Página {page}/{last_page} descargada ({len(data['data'])} capítulos)")

        all_chapters.sort(key=lambda c: float(c["name"]))
        return all_chapters
