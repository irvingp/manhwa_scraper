import os
import requests

class DownloaderService:
    def __init__(self, output_folder="output/images"):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def download_images(self, image_urls, chapter_name):
        chapter_path = os.path.join(self.output_folder, chapter_name)
        os.makedirs(chapter_path, exist_ok=True)
        image_paths = []

        for i, url in enumerate(image_urls):
            path = os.path.join(chapter_path, f"{i:03d}.webp")
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(path, "wb") as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
            image_paths.append(path)
        return image_paths
