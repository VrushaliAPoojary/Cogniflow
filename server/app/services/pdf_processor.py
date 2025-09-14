import fitz  # PyMuPDF

def extract_text_from_pdf(path: str) -> str:
    try:
        with fitz.open(path) as doc:  # ✅ ensures file is closed
            full_text = [page.get_text() for page in doc if page.get_text()]
        return "\n".join(full_text).strip()
    except Exception as e:
        print(f"❌ Error reading PDF {path}: {e}")
        return ""
