
import requests

class ImagesAPI:
    def __init__(self, base_url, headers=None, cookies=None):
        self.base_url = base_url
        self.headers = headers or {"User-Agent": "Mozilla/5.0"}
        self.cookies = cookies

    def get_images(self, chapter_id):
        url = f"{self.base_url}/{chapter_id}?type=comic"
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        response.raise_for_status()
        return response.json()["chapter"]["pages"]
