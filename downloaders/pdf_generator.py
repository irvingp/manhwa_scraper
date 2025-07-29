from PIL import Image

class PDFGenerator:
    def create_pdf_from_files(self, image_files, output_pdf):
        images = [Image.open(file).convert('RGB') for file in image_files]
        if images:
            images[0].save(output_pdf, save_all=True, append_images=images[1:])
            print(f"✅ PDF generado: {output_pdf}")
