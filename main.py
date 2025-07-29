import os
import requests
from api.chapters_api import ChaptersAPI
from downloaders.image_downloader import ImageDownloader
from downloaders.pdf_generator import PDFGenerator
from urllib.parse import urlparse

SLUG = "el-asesino-yu-ijin20250729-110824049"

BASE_URL = f"https://dashboard.olympusbiblioteca.com/api/series/{SLUG}/chapters?page=1&direction=desc&type=comic"
CHAPTER_URL_TEMPLATE = f"https://olympusbiblioteca.com/api/capitulo/{SLUG}/{{chapter_id}}?type=comic"

def extract_manwha_name(url):
    parts = urlparse(url).path.split('/')
    return parts[3] if len(parts) > 3 else "manwha"

def main():
    manwha_name = extract_manwha_name(BASE_URL)
    base_output = os.path.join("output", manwha_name)
    images_dir = os.path.join(base_output, "images")
    pdf_dir = os.path.join(base_output, "pdfs")

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)

    chapters_api = ChaptersAPI(BASE_URL)
    downloader = ImageDownloader()
    pdf_generator = PDFGenerator()

    chapters = chapters_api.get_chapters()
    print(f"📚 Total capítulos encontrados: {len(chapters)}")

    for chapter in chapters:
        chapter_id = chapter["id"]
        chapter_name = chapter["name"]
        output_pdf = os.path.join(pdf_dir, f"{chapter_name}.pdf")

        # ✅ Verificar si ya existe el PDF
        if os.path.exists(output_pdf):
            print(f"⏩ Saltando capítulo {chapter_name}, ya descargado.")
            continue

        resp = requests.get(CHAPTER_URL_TEMPLATE.format(chapter_id=chapter_id))
        resp.raise_for_status()
        data = resp.json()
        image_urls = data["chapter"]["pages"]

        print(f"⬇️ Descargando capítulo {chapter_name} ({len(image_urls)} páginas)")
        chapter_folder = os.path.join(images_dir, chapter_name)

        downloaded_files = downloader.download_chapter_images(image_urls, chapter_folder)

        pdf_generator.create_pdf_from_files(downloaded_files, output_pdf)

if __name__ == "__main__":
    main()
