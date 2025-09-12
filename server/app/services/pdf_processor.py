import fitz  # PyMuPDF
from typing import List

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    full_text = []
    for page in doc:
        txt = page.get_text()
        if txt:
            full_text.append(txt)
    return "\n".join(full_text)
