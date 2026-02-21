import img2pdf
import os

def generate_pdf(user_id: int, photo_paths: list):
    pdf_path = f"data/{user_id}/book.pdf"
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(photo_paths))
    return pdf_path