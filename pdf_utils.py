from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from a PDF file."""
    if not pdf_file:
        return ""

    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except PdfReadError:
        return "Error: Could not read the PDF file. It might be corrupted or encrypted."
    except Exception as e:
        return f"An unexpected error occurred: {e}"
