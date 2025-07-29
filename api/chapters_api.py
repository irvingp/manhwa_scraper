import requests

class ChaptersAPI:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {"User-Agent": "Mozilla/5.0"}

    def get_chapters(self, page=1):
        url = f"{self.base_url}?page={page}&direction=desc&type=comic"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["data"]  # Lista de capítulos
