from pypdf import PdfReader
import re


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    # Normalize whitespace
    full_text = re.sub(r"\s+", " ", full_text)

    return full_text.strip()
