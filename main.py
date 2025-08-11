import os
import requests
import argparse
from tqdm import tqdm
from api.chapters_api import ChaptersAPI
from downloaders.image_downloader import ImageDownloader
from downloaders.pdf_generator import PDFGenerator
from utils.helpers import extract_manwha_name, sanitize_filename
from utils.logger import get_logger

def parse_args():
    parser = argparse.ArgumentParser(description="Descarga capítulos de manhwa como PDF.")
    parser.add_argument("--slug", type=str, default="viviendo-como-un-barbaro-en-un-mundo-de-fantasia", help="SLUG de la serie")
    return parser.parse_args()

def main():
    args = parse_args()
    SLUG = args.slug
    BASE_URL = f"https://dashboard.olympusbiblioteca.com/api/series/{SLUG}/chapters?page=1&direction=desc&type=comic"
    CHAPTER_URL_TEMPLATE = f"https://olympusbiblioteca.com/api/capitulo/{SLUG}/{{chapter_id}}?type=comic"

    logger = get_logger()
    manwha_name = extract_manwha_name(BASE_URL)
    base_output = os.path.join("output", manwha_name)
    images_dir = os.path.join(base_output, "images")
    pdf_dir = os.path.join(base_output, "pdfs")

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)

    chapters_api = ChaptersAPI(BASE_URL)
    downloader = ImageDownloader()
    pdf_generator = PDFGenerator()

    try:
        chapters = chapters_api.get_chapters()
    except Exception as e:
        logger.error(f"Error obteniendo capítulos: {e}")
        print("❌ Error obteniendo capítulos.")
        return

    if not chapters:
        print("⚠️ No se encontraron capítulos.")
        return

    print(f"📚 Total capítulos encontrados: {len(chapters)}")

    for chapter in tqdm(chapters, desc="Procesando capítulos"):
        chapter_id = chapter["id"]
        chapter_name = sanitize_filename(chapter["name"])
        output_pdf = os.path.join(pdf_dir, f"{chapter_name}.pdf")

        if os.path.exists(output_pdf):
            print(f"⏩ Saltando capítulo {chapter_name}, ya descargado.")
            continue

        try:
            resp = requests.get(CHAPTER_URL_TEMPLATE.format(chapter_id=chapter_id))
            resp.raise_for_status()
            data = resp.json()
            image_urls = data["chapter"]["pages"]
        except Exception as e:
            logger.error(f"Error descargando capítulo {chapter_name}: {e}")
            print(f"❌ Error descargando capítulo {chapter_name}.")
            continue

        print(f"⬇️ Descargando capítulo {chapter_name} ({len(image_urls)} páginas)")
        chapter_folder = os.path.join(images_dir, chapter_name)

        try:
            downloaded_files = downloader.download_chapter_images(image_urls, chapter_folder)
            pdf_generator.create_pdf_from_files(downloaded_files, output_pdf)
        except Exception as e:
            logger.error(f"Error procesando imágenes/PDF para {chapter_name}: {e}")
            print(f"❌ Error procesando imágenes/PDF para {chapter_name}.")

if __name__ == "__main__":
    main()
