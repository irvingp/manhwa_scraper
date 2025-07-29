from api.chapters_api import ChaptersAPI
from api.images_api import ImagesAPI
from services.downloader import DownloaderService
from services.pdf_generator import PDFGenerator

CHAPTERS_URL = "https://dashboard.olympusbiblioteca.com/api/series/jugad20-225-reso-10000-anos-despues13424/chapters?page=2&direction=desc&type=comic"
IMAGES_URL = "https://olympusbiblioteca.com/api/capitulo/jugad20-225-reso-10000-anos-despues13424"

if __name__ == "__main__":
    chapters_api = ChaptersAPI(CHAPTERS_URL)
    images_api = ImagesAPI(IMAGES_URL)
    downloader = DownloaderService()
    pdf_gen = PDFGenerator()

    chapters = chapters_api.get_chapters()

    for chapter in chapters:
        name = chapter["name"]
        chapter_id = chapter["id"]
        print(f"📥 Procesando capítulo {name}...")

        images = images_api.get_images(chapter_id)
        image_paths = downloader.download_images(images, name)
        pdf_path = pdf_gen.create_pdf(image_paths, name)

        print(f"✅ PDF creado: {pdf_path}")
