from fpdf import FPDF
from PIL import Image
import os

class PDFGenerator:
    def __init__(self, output_folder="output/pdfs"):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def create_pdf(self, image_paths, chapter_name):
        pdf = FPDF()
        for img in image_paths:
            cover = Image.open(img)
            width, height = cover.size
            pdf.add_page(format=(width * 0.264583, height * 0.264583))
            pdf.image(img, 0, 0, width * 0.264583, height * 0.264583)

        output_path = os.path.join(self.output_folder, f"{chapter_name}.pdf")
        pdf.output(output_path, "F")
        return output_path
